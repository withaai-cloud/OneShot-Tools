#!/usr/bin/env python3
"""
OneShot Tools - Web Application
A collection of useful productivity tools
"""

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
import sys
import re
import pypdfium2 as pdfium
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import zipfile
from io import BytesIO

# Get the absolute path of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

# Determine template and static directories
# On Vercel, we're called from api/index.py, but app.py is at root
# Templates are in api/templates
template_dir = None
static_dir = None

# Try api/templates first (Vercel structure)
if os.path.exists(os.path.join(basedir, 'api', 'templates')):
    template_dir = os.path.join(basedir, 'api', 'templates')
    static_dir = os.path.join(basedir, 'api', 'static')
# Try templates at root (local development)
elif os.path.exists(os.path.join(basedir, 'templates')):
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
# Last resort: check if we're in parent of api folder
elif os.path.exists(os.path.join(os.path.dirname(basedir), 'api', 'templates')):
    parent = os.path.dirname(basedir)
    template_dir = os.path.join(parent, 'api', 'templates')
    static_dir = os.path.join(parent, 'api', 'static')
else:
    # Default fallback
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')

# Create Flask app with explicit template and static paths
app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)
            
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Use /tmp for Vercel deployment (writable directory)
import tempfile
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['OUTPUT_FOLDER'] = tempfile.gettempdir()

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def extract_transactions_from_pdf(pdf_path, invert_amounts=False):
    """Extract transaction data from FNB bank statement PDF"""
    
    transactions = []
    statement_year = None
    
    # Open the PDF
    pdf = pdfium.PdfDocument(pdf_path)
    
    # Process each page
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        
        # Extract year from statement period (only on first page)
        if page_num == 0 and not statement_year:
            year_match = re.search(r'Statement Period.*?(\d{4})', text)
            if year_match:
                statement_year = year_match.group(1)
        
        # Split into lines
        lines = text.split('\n')
        
        # Look for transaction lines
        for i, line in enumerate(lines):
            # Pattern to match date at start of line (DD Mon format)
            date_pattern = r'^(\d{2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\s+'
            
            match = re.match(date_pattern, line)
            if match:
                date_str = match.group(1)
                
                # Extract the rest of the line after the date
                remainder = line[len(date_str):].strip()
                
                # Split remainder to get description and amount
                parts = remainder.split()
                
                if len(parts) >= 2:
                    # Find amount - looking for pattern with digits, commas, decimals
                    amount_pattern = r'[\d,]+\.\d{2}(?:Cr|Dr)?'
                    
                    # Search from the end of parts
                    amount = None
                    description_parts = []
                    balance_found = False
                    
                    for j in range(len(parts) - 1, -1, -1):
                        part = parts[j]
                        
                        # Check if this looks like a monetary amount
                        if re.match(amount_pattern, part):
                            if not balance_found and not amount:
                                # This is likely the balance (last monetary value)
                                balance_found = True
                                continue
                            elif balance_found and not amount:
                                # This is the amount (second to last monetary value)
                                amount = part
                                # Everything before this is description
                                description_parts = parts[:j]
                                break
                        
                    # If we found an amount, save the transaction
                    if amount:
                        description = ' '.join(description_parts)
                        
                        # Handle empty descriptions
                        if not description or description.strip() == '':
                            description = '#Monthly Account Fee'
                        
                        # Convert date format from "01 Jun" to "01/06/2024"
                        month_map = {
                            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                        }
                        
                        date_parts = date_str.split()
                        if len(date_parts) == 2:
                            day = date_parts[0]
                            month_abbr = date_parts[1]
                            month = month_map.get(month_abbr, '01')
                            formatted_date = f"{day}/{month}/{statement_year}"
                        else:
                            formatted_date = date_str
                        
                        # Clean up amount - remove "Cr" suffix for credits
                        is_credit = 'Cr' in amount
                        amount_clean = amount.replace('Cr', '').replace('Dr', '')
                        
                        # If it's a debit (no Cr suffix), make it negative
                        if not is_credit:
                            amount_clean = '-' + amount_clean
                        
                        # Apply inversion if requested
                        if invert_amounts:
                            try:
                                amount_val = float(amount_clean.replace(',', ''))
                                amount_val = -amount_val
                                amount_clean = str(amount_val)
                            except:
                                pass
                        
                        transactions.append({
                            'Date': formatted_date,
                            'Description': description,
                            'Amount': amount_clean
                        })
    
    return transactions

def create_excel_file(transactions, output_path):
    """Create Excel file with extracted transactions"""
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Bank Statement"
    
    # Define headers
    headers = ['Date', 'Description', 'Amount']
    
    # Style for headers
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=12)
    
    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Write transaction data
    for row_num, transaction in enumerate(transactions, 2):
        ws.cell(row=row_num, column=1, value=transaction['Date'])
        ws.cell(row=row_num, column=2, value=transaction['Description'])
        
        # Convert amount to number for Excel
        amount_str = transaction['Amount'].replace(',', '')
        try:
            amount_num = float(amount_str)
            cell = ws.cell(row=row_num, column=3, value=amount_num)
            # Format as currency
            cell.number_format = '#,##0.00'
        except:
            ws.cell(row=row_num, column=3, value=transaction['Amount'])
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 15
    
    # Save workbook
    wb.save(output_path)

@app.route('/')
def index():
    """Homepage"""
    try:
        # Debug: Check if template exists
        template_path = os.path.join(app.template_folder, 'index.html')
        if not os.path.exists(template_path):
            return f"Template not found at: {template_path}<br>Base dir: {basedir}<br>Template folder: {app.template_folder}<br>Files in dir: {os.listdir(basedir)}", 500
        return render_template('index.html')
    except Exception as e:
        import traceback
        return f"Error: {str(e)}<br><br>Traceback:<br><pre>{traceback.format_exc()}</pre><br>Template folder: {app.template_folder}<br>Base dir: {basedir}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'OneShot Tools is running',
        'python_version': sys.version
    })

@app.route('/tools/bank-statement-converter')
def bank_statement_converter():
    """Bank Statement Converter Tool"""
    return render_template('bank_statement_converter.html')

@app.route('/tools/tax-optimizer')
def tax_optimizer():
    """SA Tax Split Optimizer Tool"""
    return render_template('tax_optimizer.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Handle PDF conversion"""
    try:
        # Check if files were uploaded
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Get invert option
        invert_amounts = request.form.get('invert_amounts') == 'true'
        
        # Process all files
        output_files = []
        all_transactions = []
        
        for file in files:
            if file and file.filename.endswith('.pdf'):
                # Save uploaded file
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract transactions
                transactions = extract_transactions_from_pdf(filepath, invert_amounts)
                all_transactions.extend(transactions)
                
                # Create Excel file
                output_filename = filename.replace('.pdf', '_transactions.xlsx')
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                create_excel_file(transactions, output_path)
                
                output_files.append({
                    'original': filename,
                    'output': output_filename,
                    'transactions': len(transactions)
                })
                
                # Clean up uploaded file
                os.remove(filepath)
        
        # If multiple files, create a combined Excel and a ZIP
        if len(output_files) > 1:
            # Create combined Excel
            combined_filename = f'combined_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            combined_path = os.path.join(app.config['OUTPUT_FOLDER'], combined_filename)
            create_excel_file(all_transactions, combined_path)
            
            # Create ZIP file with all outputs
            zip_filename = f'all_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
            zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                # Add combined file
                zipf.write(combined_path, combined_filename)
                
                # Add individual files
                for output_file in output_files:
                    file_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file['output'])
                    zipf.write(file_path, output_file['output'])
            
            return jsonify({
                'success': True,
                'multiple': True,
                'files': output_files,
                'combined': combined_filename,
                'zip': zip_filename,
                'total_transactions': len(all_transactions)
            })
        else:
            # Single file
            return jsonify({
                'success': True,
                'multiple': False,
                'file': output_files[0]['output'],
                'transactions': output_files[0]['transactions']
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Download converted file"""
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#!/usr/bin/env python3
"""
OneShot Tools - Web Application
A collection of useful productivity tools
"""

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
import sys
import re
import csv
import pypdfium2 as pdfium
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import zipfile
from io import BytesIO, StringIO

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

def decode_absa_text(text):
    """Decode garbled ABSA PDF text to readable characters"""
    char_map = {
        # Digits
        'ð': '0', 'ñ': '1', 'ò': '2', 'ó': '3', 'ô': '4',
        'õ': '5', 'ö': '6', '÷': '7', 'ø': '8', 'ù': '9',
        
        # Special characters
        'a': '/', 'k': '.', 'K': '.', '@': ' ', '`': '-', 'z': ':',
        '\\': '*', 'm': 'j',
        
        # Control characters (0x80-0x9F range) - lowercase letters
        '\x81': 'a',
        '\x82': 'b',
        '\x83': 'c',
        '\x84': 'o',
        '\x85': 'e',
        '\x86': 'i',
        '\x87': 'g',
        '\x88': 'h',
        '\x89': 'i',
        '\x8a': 'j',
        '\x8b': 'k',
        '\x8c': 'w',
        '\x8d': 'd',
        '\x8e': 'f',
        '\x8f': 'p',
        '\x90': 'v',
        '\x91': 'm',
        '\x92': 'a',
        '\x93': 'r',
        '\x94': 's',
        '\x95': 'n',
        '\x96': 'u',
        '\x97': 'y',
        '\x98': 'l',
        '\x99': 'r',
        
        # Uppercase letters
        'Á': 'A', 'Â': 'B', 'Ã': 'C', 'Ä': 'D', 'Å': 'E',
        'Æ': 'F', 'Ç': 'G', 'È': 'H', 'É': 'I', 'Ê': 'J',
        'Ë': 'K', 'Ì': 'L', 'Í': 'M', 'Î': 'N', 'Ï': 'O',
        'Ñ': 'P', 'Ò': 'Q', 'Ó': 'R', 'Ô': 'S', 'Õ': 'T',
        'Ö': 'U', '×': 'V', 'Ø': 'W', 'Ù': 'X', 'Ú': 'Y', 'Û': 'Z',
        
        # Lowercase letters (extended ASCII)
        'â': 'S', 'ã': 'T', 'å': 'W', 'æ': 'H', 'ç': 'N', 'è': 'Y',
        '¢': 'e', '£': 't', '¤': 'a', '¥': 'r', '¦': 'w', '§': 'x',
        '¨': 'n', '©': 'o', 'ª': 'i', '«': 'u', '¬': 's', '­': 'd',
        '®': 'l', '¯': 'c', '°': 'f', '±': 'h', '²': 'm', '³': 'p',
        '´': 'g', 'µ': 'b', '¶': 'v', '·': 'k', '¸': 'x', '¹': 'j',
        'º': 'q', '»': 'z',
    }
    
    result = ''
    for char in text:
        result += char_map.get(char, char)
    return result

def detect_bank_format(text):
    """Detect if the statement is from FNB, ABSA, or Standard Bank"""
    # Check for official bank identifiers first (more specific)
    if 'FNB FUSION' in text.upper() or 'FIRST NATIONAL BANK' in text.upper():
        return 'FNB'
    elif 'STANDARD BANK' in text.upper():
        return 'STANDARD_BANK'
    elif 'ABSA BANK' in text or 'Absa Bank' in text:
        return 'ABSA'
    # Fallback to less specific checks
    elif 'FNB' in text.upper():
        return 'FNB'
    elif 'ABSA' in text.upper():
        return 'ABSA'
    # Default to FNB if unclear
    return 'FNB'

def extract_transactions_from_absa(pdf_path, invert_amounts=False, statement_year='auto'):
    """Extract transaction data from ABSA bank statement PDF"""
    
    transactions = []
    detected_year = None
    
    # Open the PDF
    pdf = pdfium.PdfDocument(pdf_path)
    
    # Combine all pages into one text block to handle cross-page continuations
    all_text = []
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        
        # Decode the garbled text
        text = decode_absa_text(text)
        
        # Extract year from statement period (first page only)
        if page_num == 0 and not detected_year:
            year_match = re.search(r'(\d{1,2})\s+\w+\s+(\d{4})\s+to', text)
            if year_match:
                detected_year = year_match.group(2)
        
        all_text.append(text)
    
    # Use override year if provided, otherwise use detected year
    year_to_use = statement_year if statement_year != 'auto' else detected_year
    
    # Join all pages with a special marker so we know where page breaks are
    combined_text = '\n'.join(all_text)
    lines = combined_text.split('\n')
    
    # Look for transaction lines
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # ABSA date pattern: DD/MM/YYYY at start of line
        date_pattern = r'^(\d{1,2}/\d{2}/\d{4})\s+'
        
        match = re.match(date_pattern, line)
        if match:
            date_str = match.group(1)
            
            # Extract the rest of the line after the date
            remainder = line[len(date_str):].strip()
            
            # Get description (everything before the amounts)
            description_parts = []
            
            # First part of description is on this line
            desc_match = re.match(r'^([A-Za-z\s:]+)', remainder)
            if desc_match:
                description_parts.append(desc_match.group(1).strip())
            
            # Check for continuation lines (can cross page boundaries!)
            j = i + 1
            continuation_count = 0
            consecutive_non_continuation = 0
            max_continuations = 10
            
            while j < len(lines) and continuation_count < max_continuations:
                next_line = lines[j].strip()
                
                # Stop if it's a new date line
                if re.match(date_pattern, next_line):
                    break
                
                # Stop if it's empty
                if not next_line:
                    j += 1
                    consecutive_non_continuation += 1
                    if consecutive_non_continuation > 30:  # Too many empty lines
                        break
                    continue
                
                # Check if line contains descriptive text
                has_text = re.search(r'[A-Za-z]{3,}', next_line)
                
                if has_text:
                    # Filter out metadata/header/footer lines
                    if any(kw in next_line for kw in ['Charge Statement Detail', 'Se Ttiine', 'MEiiectire', 'Cheae accant', 'Cheae Accant', 'YUäX VXICITG', 'SIXAC', 'QRIV STXEET', 'WXYHEID', '41-0214-4229', '197', '3100', 'Xetarn aooreee', 'Accant Tne', 'Stateent n', 'WAT reg n', 'Urerorait', 'Deecritin Charge Debit Aant', 'Ieeaeo', 'VXICITG VRAT', 'ITTEXEST XATE', 'ITCRäDED', 'CHAXGE:', 'ADSITISTXATIUT', 'CASH DEVUSIT', 'SINED', 'SEXWICE', 'TXATSACTIUT', 'Date Traneactin', 'SVXUVE', 'Bana Riiteo', 'Aathrieeo Financia', 'Xegietereo Creoit', 'Xegietratin Taber', 'CSV001CW', 'traneactine Mcntinaeo', 'Vage', 'Tax Inrice', 'eSt/jp', 'Gener/l Enquiries', '08600', 'Uar Vriracn', 'Wieit abea', 'Baance', 'Accant Saarn', 'Yar traneactine']):
                        # Metadata - skip and increment non-continuation counter
                        consecutive_non_continuation += 1
                        # If we've hit too many non-continuation lines, stop
                        if consecutive_non_continuation > 10:
                            break
                        j += 1
                        continue
                    else:
                        # Real continuation line
                        description_parts.append(next_line)
                        continuation_count += 1
                        consecutive_non_continuation = 0  # Reset counter
                        
                        # Stop if this line ends with a known ending pattern
                        # Date patterns: "5 Aug", "5 March", "5 Sept", location names, etc.
                        if re.search(r'(Njala|Garage|Holland\d+|\d+\s+(Aag|Aug|March|Sarch|Sept|Pa|Jan|Feb|Apr|May|Jun|Jul|Oct|Nov|Dec|Paye))$', next_line.strip(), re.IGNORECASE):
                            # This is the end of the description
                            j += 1
                            break
                    j += 1
                else:
                    # No text
                    consecutive_non_continuation += 1
                    if consecutive_non_continuation > 10:
                        break
                    j += 1
            
            # Update index to skip processed continuation lines
            i = j - 1
            
            # Combine description parts
            description = ' '.join(description_parts)
            
            # Clean up description
            description = description.replace('Setteent', 'Settlement')
            description = description.replace('Heaoiiice', 'Headoffice')
            description = description.replace('Archire', 'Archive')
            description = description.replace('Ttiiic', 'Notific')
            description = description.replace('Ttiine', 'Notifyme')
            description = description.replace('Vanent', 'Payment')
            description = description.replace('Vane ', 'Payee ')
            description = description.replace('Tranei', 'Transf')
            description = description.replace('Varchaee', 'Purchase')
            description = description.replace('Creoit', 'Credit')
            description = description.replace('Externa', 'External')
            description = description.replace('Digita', 'Digital')
            description = description.replace('Snthn', 'Monthly')
            description = description.replace('Traneactin', 'Transaction')
            description = description.replace('Aoin', 'Admin')
            description = description.replace('Vri Ui Vt Eai', 'Proof Of Pmt Email')
            description = description.replace('Ve', 'Pos')
            description = description.replace('Haro', 'Holland')
            description = description.replace('Heebanajii', 'Holland')
            description = description.replace('Eto', 'Edo')
            description = description.replace('Ba Braght Frwaro', 'Bal Brought Forward')
            description = description.replace('Abea Bana', 'Absa Bank')
            description = description.replace('Sare', 'Sars')
            description = description.replace('Stars', 'Sars')
            description = description.replace('Traneier', 'Transfer')
            description = description.replace('Sarch', 'March')
            description = description.replace('Aag', 'Aug')
            description = description.replace('Uct', 'Oct')
            description = description.replace('Pan', 'Jan')  # Fixed: Pan -> Jan
            description = description.replace('Caro T.', 'Card No.')
            description = description.replace('Caro ', 'Card ')
            description = description.replace('Stegene', 'Stegens')
            description = description.replace('Stegen ', 'Stegens ')
            description = description.replace('Wrnhe', 'Vryhe')
            description = description.replace('Vryheio', 'Vryheid')
            description = description.replace('MEii', 'Vyh')
            description = description.replace('Stateent Detai', 'Statement Detail')
            description = description.replace('Tmaa', 'Njala')
            description = description.replace('Hbane', 'Hlobane')
            description = description.replace('Deetiart', 'Desti')
            description = description.replace('Vara', 'Park')
            description = description.replace('Santa', 'Santam')
            description = description.replace('Qieeie', 'Kommissie')
            description = description.replace('Saio', 'Suid')
            description = description.replace('äitanoer', 'Uitlander')
            
            # Complex merchant name fixes
            description = description.replace('Sagg Ano Bean', 'Mugg And Bean')
            description = description.replace('Sar Goen Posaa', 'Spur Golden Peak')  # Fixed
            description = description.replace('Siririer Cnre', 'Mooirivier Conve')
            description = description.replace('Sirrier Cnre', 'Mooirivier Conve')
            description = description.replace('Vtch', 'Potch')
            description = description.replace('Hhee', 'Wheel')
            description = description.replace('Chain Wheel  P  Tyr', 'Champion Wheel & Tyr')
            description = description.replace('Tnr', 'Tyr')
            description = description.replace('Sirac Vr', 'Mirac Prop')
            
            # Bank/Digital payment specific fixes
            description = description.replace('Cat 5 Dec', 'Comput 5 Dec')  # Fixed: Cat -> Comput
            description = description.replace('Cat 5 March', 'Comput 5 March')
            description = description.replace('Cat 4 Set', 'Comput 4 Sept')
            
            # Bank name fixes - order matters!
            description = description.replace('Holland85344807104', 'Wesbank_fi85344807104')
            description = description.replace('Ribertn', 'Liberty')
            
            # Find ALL amounts in the line
            amount_pattern = r'(\d{1,3}(?:[\s,]\d{3})*\.\d{2})'
            all_amounts = re.findall(amount_pattern, line)
            
            # Clean amounts
            all_amounts = [a.replace(' ', ',') for a in all_amounts]
            
            # CRITICAL: Column structure is:
            # Charge (col 3) | Debit (col 4) | Credit (col 5) | Balance (col 6)
            
            final_amount = None
            
            if len(all_amounts) == 0:
                # No amounts - skip
                i += 1
                continue
                
            elif len(all_amounts) == 1:
                # Only balance - skip (no debit or credit)
                i += 1
                continue
                
            elif len(all_amounts) == 2:
                # Two amounts: Could be:
                # 1. Charge + Balance (has A or T marker) - SKIP
                # 2. Debit + Balance (has * marker or no marker) - EXTRACT as negative
                # 3. Credit + Balance (Transf/Transfer in description) - EXTRACT as positive
                
                # Check if line has asterisk (bank charges) - these are debits
                if '*' in line:
                    # Bank charge: Debit + Balance - extract first as negative
                    final_amount = '-' + all_amounts[0]
                # Check if this is a credit transaction (Transfer/Credit without charge)
                elif 'Credit' in description or 'Deposit' in description or 'Transf' in description or 'Transfer' in description:
                    # Credit + Balance - extract first amount as positive
                    final_amount = all_amounts[0]  # Positive
                # Check if line has charge indicator (A or T)
                elif ' A ' in line or ' T ' in line:
                    # Charge + Balance - skip
                    i += 1
                    continue
                else:
                    # Debit + Balance (no marker) - extract as negative
                    final_amount = '-' + all_amounts[0]
                    
            elif len(all_amounts) == 3:
                # Charge + Debit/Credit + Balance
                # Example: 15.00 T 944.27 342,616.71
                # Middle amount (index 1) is the debit or credit
                transaction_amount = all_amounts[1]
                
                # Determine if it's debit (negative) or credit (positive)
                if 'Credit' in description or 'Deposit' in description:
                    final_amount = transaction_amount  # Positive
                else:
                    final_amount = '-' + transaction_amount  # Negative
                    
            elif len(all_amounts) >= 4:
                # Rare case: might have multiple amounts
                # Assume second-to-last is transaction, last is balance
                transaction_amount = all_amounts[-2]
                
                if 'Credit' in description or 'Deposit' in description:
                    final_amount = transaction_amount  # Positive
                else:
                    final_amount = '-' + transaction_amount  # Negative
            
            # Skip if no valid transaction amount
            if not final_amount:
                i += 1
                continue
            
            # Skip balance brought forward
            if 'Brought Forward' in description or 'Braght Frwaro' in description:
                i += 1
                continue
            
            if description.strip():
                # Apply inversion if requested
                if invert_amounts:
                    try:
                        amount_val = float(final_amount.replace(',', ''))
                        amount_val = -amount_val
                        if amount_val >= 0:
                            final_amount = f"{amount_val:,.2f}"
                        else:
                            final_amount = f"-{abs(amount_val):,.2f}"
                    except:
                        pass
                
                transactions.append({
                    'Date': date_str,
                    'Description': description.strip(),
                    'Amount': final_amount
                })
        
        i += 1
    
    return transactions

def extract_transactions_from_pdf(pdf_path, invert_amounts=False, statement_year='auto'):
    """Extract transaction data from bank statement PDF (supports FNB, ABSA, and Standard Bank)"""
    
    # Read first page to detect bank format
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[0]
    textpage = page.get_textpage()
    text = textpage.get_text_range()
    
    bank_format = detect_bank_format(text)
    
    if bank_format == 'ABSA':
        return extract_transactions_from_absa(pdf_path, invert_amounts, statement_year)
    elif bank_format == 'STANDARD_BANK':
        return extract_transactions_from_standard_bank(pdf_path, invert_amounts, statement_year)
    else:
        return extract_transactions_from_fnb(pdf_path, invert_amounts, statement_year)

def extract_transactions_from_standard_bank(pdf_path, invert_amounts=False, statement_year='auto'):
    """Extract transaction data from Standard Bank statement PDF"""
    
    transactions = []
    detected_end_year = None
    statement_start_month = None
    statement_end_month = None
    
    # Open the PDF
    pdf = pdfium.PdfDocument(pdf_path)
    
    # Combine all pages
    all_text = []
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        
        # Extract year and month range from first page
        if page_num == 0:
            # Look for "From: 30 Oct 25" and "To: 28 Jan 26"
            from_match = re.search(r'From:\s+\d{1,2}\s+(\w+)\s+(\d{2})', text)
            to_match = re.search(r'To:\s+\d{1,2}\s+(\w+)\s+(\d{2})', text)
            
            if to_match:
                statement_end_month = to_match.group(1)
                year_suffix = to_match.group(2)
                detected_end_year = '20' + year_suffix
            
            if from_match:
                statement_start_month = from_match.group(1)
        
        all_text.append(text)
    
    # Use override year if provided, otherwise use detected year
    statement_end_year = statement_year if statement_year != 'auto' else detected_end_year
    
    combined_text = '\n'.join(all_text)
    lines = combined_text.split('\n')
    
    # Process lines
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Standard Bank date pattern: "30 Oct 25" or "01 Nov 25"
        date_pattern = r'^(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2})\s+'
        
        match = re.match(date_pattern, line)
        if match:
            date_str = match.group(1)
            
            # Get description from this line (after date)
            desc_parts = []
            remainder = line[len(date_str):].strip()
            if remainder and remainder != 'Date Description Payments Deposits Balance':
                desc_parts.append(remainder)
            
            # Check next lines for description continuation and amount
            j = i + 1
            amount = None
            
            # Skip known metadata lines that are part of the transaction
            metadata_keywords = [
                'FEE:', 'IMMEDIATE PAYMENT', 'IB PAYMENT', 'CREDIT TRANSFER', 
                'DEBIT TRANSFER', 'REAL TIME TRANSFER', 'ELECTRONIC TRF',
                'INSURANCE PREMIUM', 'MONTHLY MANAGEMENT', 'SERVICE FEE'
            ]
            
            while j < len(lines) and j < i + 5:  # Look ahead max 5 lines
                next_line = lines[j].strip()
                
                if not next_line:
                    j += 1
                    continue
                
                # Check if this line is a new transaction (starts with date)
                if re.match(date_pattern, next_line):
                    break
                
                # Check if this line contains amount (has number with commas)
                # Standard Bank format: either just deposit or -payment followed by balance
                # Pattern: "-1,800.00 41,865.05" or "32,680.00 43,665.05"
                amount_pattern = r'^(-?\d{1,3}(?:,\d{3})*\.\d{2})\s+\d{1,3}(?:,\d{3})*\.\d{2}$'
                amount_match = re.search(amount_pattern, next_line)
                
                if amount_match:
                    # This is the amount line
                    amount = amount_match.group(1)
                    j += 1
                    break
                else:
                    # Check if it's a metadata line
                    is_metadata = any(keyword in next_line for keyword in metadata_keywords)
                    
                    if not is_metadata and not next_line.startswith('ACC '):
                        # This is a description continuation
                        if len(next_line) > 3:
                            desc_parts.append(next_line)
                    j += 1
            
            # Update main index
            i = j
            
            # Skip if no amount found
            if not amount:
                continue
            
            # Combine description
            description = ' '.join(desc_parts).strip()
            
            # Skip opening balance
            if 'OPENING BALANCE' in description.upper() or 'STATEMENT OPENING' in description.upper():
                continue
            
            # Skip if description is empty
            if not description or description == 'Date Description Payments Deposits Balance':
                continue
            
            # Clean up description
            description = description.replace('  ', ' ')
            
            # Convert date from "30 Oct 25" to "30/10/2025"
            try:
                # Parse the date string
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                
                # Month order for year rollover detection
                month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                # Split "30 Oct 25" into parts
                parts = date_str.split()
                if len(parts) == 3:
                    day = parts[0].zfill(2)
                    month_name = parts[1]
                    month = month_map.get(month_name, '01')
                    
                    # Determine year based on month
                    # If transaction month comes before the end month, it's the previous year
                    # Example: Statement "Oct 25 to Jan 26" - Oct/Nov/Dec are 2025, Jan is 2026
                    if statement_end_year and statement_end_month and statement_start_month:
                        end_month_idx = month_order.index(statement_end_month) if statement_end_month in month_order else 0
                        curr_month_idx = month_order.index(month_name) if month_name in month_order else 0
                        
                        # If current month > end month, it's in the previous year
                        if curr_month_idx > end_month_idx:
                            year = str(int(statement_end_year) - 1)
                        else:
                            year = statement_end_year
                    else:
                        # Fallback to year from date string
                        year = '20' + parts[2]
                    
                    date_str = f"{day}/{month}/{year}"
            except:
                # If conversion fails, keep original format
                pass
            
            # Apply inversion if requested
            if invert_amounts:
                try:
                    amount_val = float(amount.replace(',', ''))
                    amount_val = -amount_val
                    amount = f"{amount_val:,.2f}"
                except:
                    pass
            
            transactions.append({
                'Date': date_str,
                'Description': description,
                'Amount': amount
            })
        else:
            i += 1
    
    return transactions

def extract_transactions_from_fnb(pdf_path, invert_amounts=False, statement_year='auto'):
    """Extract transaction data from FNB bank statement PDF"""
    
    transactions = []
    detected_year = None
    
    # Open the PDF
    pdf = pdfium.PdfDocument(pdf_path)
    
    # First, detect the year from first page
    first_page = pdf[0]
    first_textpage = first_page.get_textpage()
    first_text = first_textpage.get_text_range()
    
    year_match = re.search(r'Statement Period.*?(\d{4})', first_text)
    if year_match:
        detected_year = year_match.group(1)
    
    # Use override year if provided, otherwise use detected year
    year_to_use = statement_year if statement_year != 'auto' else detected_year
    
    # Process each page
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        
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
                            formatted_date = f"{day}/{month}/{year_to_use}"
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
                                # Remove commas and convert to float
                                amount_val = float(amount_clean.replace(',', ''))
                                # Invert the sign
                                amount_val = -amount_val
                                # Format with commas
                                if amount_val >= 0:
                                    amount_clean = f"{amount_val:,.2f}"
                                else:
                                    amount_clean = f"-{abs(amount_val):,.2f}"
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
        
        # Get invert option - FormData sends boolean as string
        invert_amounts_str = request.form.get('invert_amounts', 'false')
        invert_amounts = invert_amounts_str.lower() == 'true'
        
        # Get output format option
        output_format = request.form.get('output_format', 'excel')  # Default to excel
        
        # Get statement year option
        statement_year = request.form.get('statement_year', 'auto')  # Default to auto
        
        # Debug: log the settings
        print(f"DEBUG: invert_amounts_str = '{invert_amounts_str}', invert_amounts = {invert_amounts}")
        print(f"DEBUG: output_format = '{output_format}'")
        print(f"DEBUG: statement_year = '{statement_year}'")
        
        # Process all files
        output_files = []
        all_transactions = []
        file_data = {}  # Store file data in memory
        
        for file in files:
            if file and file.filename.endswith('.pdf'):
                # Save uploaded file temporarily
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract transactions with optional year override
                transactions = extract_transactions_from_pdf(filepath, invert_amounts, statement_year)
                all_transactions.extend(transactions)
                
                # Create output file based on format
                if output_format == 'csv':
                    output_filename = filename.replace('.pdf', '_transactions.csv')
                    # Create CSV in memory
                    csv_buffer = StringIO()
                    csv_writer = csv.writer(csv_buffer)
                    
                    # Write headers
                    csv_writer.writerow(['Date', 'Description', 'Amount'])
                    
                    # Write data
                    for transaction in transactions:
                        csv_writer.writerow([
                            transaction['Date'],
                            transaction['Description'],
                            transaction['Amount']
                        ])
                    
                    # Store in memory as base64
                    import base64
                    csv_content = csv_buffer.getvalue()
                    file_data[output_filename] = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
                    
                else:  # Excel format
                    output_filename = filename.replace('.pdf', '_transactions.xlsx')
                    
                    # Create workbook
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Bank Statement"
                    
                    # Headers
                    headers = ['Date', 'Description', 'Amount']
                    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
                    header_font = Font(bold=True, color='FFFFFF', size=12)
                    
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num, value=header)
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = Alignment(horizontal='center', vertical='center')
                    
                    # Data
                    for row_num, transaction in enumerate(transactions, 2):
                        ws.cell(row=row_num, column=1, value=transaction['Date'])
                        ws.cell(row=row_num, column=2, value=transaction['Description'])
                        
                        amount_str = transaction['Amount'].replace(',', '')
                        try:
                            amount_num = float(amount_str)
                            cell = ws.cell(row=row_num, column=3, value=amount_num)
                            cell.number_format = '#,##0.00'
                        except:
                            ws.cell(row=row_num, column=3, value=transaction['Amount'])
                    
                    # Column widths
                    ws.column_dimensions['A'].width = 12
                    ws.column_dimensions['B'].width = 50
                    ws.column_dimensions['C'].width = 15
                    
                    # Save to BytesIO
                    excel_buffer = BytesIO()
                    wb.save(excel_buffer)
                    excel_buffer.seek(0)
                    
                    # Store in memory
                    import base64
                    file_data[output_filename] = base64.b64encode(excel_buffer.read()).decode('utf-8')
                
                output_files.append({
                    'original': filename,
                    'output': output_filename,
                    'transactions': len(transactions)
                })
                
                # Clean up uploaded file
                os.remove(filepath)
        
        # If multiple files, create a combined file and a ZIP
        if len(output_files) > 1:
            # Create combined file based on format
            if output_format == 'csv':
                combined_filename = f'combined_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                
                csv_buffer = StringIO()
                csv_writer = csv.writer(csv_buffer)
                
                # Write headers
                csv_writer.writerow(['Date', 'Description', 'Amount'])
                
                # Write all transactions
                for transaction in all_transactions:
                    csv_writer.writerow([
                        transaction['Date'],
                        transaction['Description'],
                        transaction['Amount']
                    ])
                
                import base64
                csv_content = csv_buffer.getvalue()
                file_data[combined_filename] = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
                
            else:  # Excel format
                combined_filename = f'combined_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                
                wb = Workbook()
                ws = wb.active
                ws.title = "Bank Statement"
                
                headers = ['Date', 'Description', 'Amount']
                header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
                header_font = Font(bold=True, color='FFFFFF', size=12)
                
                for col_num, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col_num, value=header)
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                
                for row_num, transaction in enumerate(all_transactions, 2):
                    ws.cell(row=row_num, column=1, value=transaction['Date'])
                    ws.cell(row=row_num, column=2, value=transaction['Description'])
                    
                    amount_str = transaction['Amount'].replace(',', '')
                    try:
                        amount_num = float(amount_str)
                        cell = ws.cell(row=row_num, column=3, value=amount_num)
                        cell.number_format = '#,##0.00'
                    except:
                        ws.cell(row=row_num, column=3, value=transaction['Amount'])
                
                ws.column_dimensions['A'].width = 12
                ws.column_dimensions['B'].width = 50
                ws.column_dimensions['C'].width = 15
                
                excel_buffer = BytesIO()
                wb.save(excel_buffer)
                excel_buffer.seek(0)
                
                import base64
                file_data[combined_filename] = base64.b64encode(excel_buffer.read()).decode('utf-8')
            
            # Create ZIP in memory
            zip_filename = f'all_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add combined file
                zipf.writestr(combined_filename, base64.b64decode(file_data[combined_filename]))
                
                # Add individual files
                for output_file in output_files:
                    zipf.writestr(output_file['output'], base64.b64decode(file_data[output_file['output']]))
            
            zip_buffer.seek(0)
            file_data[zip_filename] = base64.b64encode(zip_buffer.read()).decode('utf-8')
            
            return jsonify({
                'success': True,
                'multiple': True,
                'files': output_files,
                'combined': combined_filename,
                'zip': zip_filename,
                'total_transactions': len(all_transactions),
                'file_data': file_data  # Send file data directly
            })
        else:
            # Single file
            return jsonify({
                'success': True,
                'multiple': False,
                'file': output_files[0]['output'],
                'transactions': output_files[0]['transactions'],
                'file_data': file_data  # Send file data directly
            })
            
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/download/<filename>')
def download(filename):
    """Download converted file"""
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

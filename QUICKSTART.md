# 🚀 Quick Start Guide - OneShot Tools

## Getting Started in 3 Steps

### Step 1: Install Python (if not already installed)
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### Step 2: Run the Application

**On Windows:**
- Double-click `start.bat`

**On Mac/Linux:**
- Open Terminal
- Navigate to the oneshot-tools folder
- Run: `bash start.sh`

**Or manually:**
```bash
cd oneshot-tools
pip install flask pypdfium2 openpyxl
python app.py
```

### Step 3: Open in Browser
- Go to: **http://localhost:5000**
- That's it! 🎉

## Using the Tools

### Bank Statement Converter

1. Click "Bank Statement Converter" on the homepage
2. Upload your PDF bank statement(s):
   - Drag & drop files OR
   - Click "Select Files"
3. Optional: Check "Invert amounts" if needed
4. Click "Convert to Excel"
5. Download your converted file(s)

**Multiple Files:**
When you upload multiple PDFs, you get:
- ✅ Individual Excel file for each PDF
- ✅ Combined Excel with all transactions
- ✅ ZIP file with everything

### SA Tax Split Optimizer

1. Click "SA Tax Split Optimizer" on the homepage
2. Enter your total annual income (in Rands)
3. Click "Calculate Optimal Split"
4. View your results:
   - Optimal split between Individual and SBC tax
   - Tax payable for each structure
   - Total tax and effective rate
   - Potential savings

**Perfect for:**
- Small business owners
- Freelancers with multiple income sources
- Tax planning and optimization
- Understanding tax implications

## Tips & Tricks

### Amount Inversion
Use this when you need to flip all amounts:
- Credits become debits
- Debits become credits
Perfect for different accounting systems!

### Supported Formats

**Bank Statement Converter:**
- FNB (First National Bank) statements

**Tax Optimizer:**
- 2024/2025 SA Individual tax brackets
- SBC (Small Business Corporation) tax rates

More bank formats and tools coming soon!

### Troubleshooting

**App won't start?**
- Make sure Python is installed
- Try: `pip install flask pypdfium2 openpyxl`

**Can't upload files?**
- Check file is PDF format
- Max file size: 50MB
- Try fewer files at once

**Missing transactions?**
- Verify it's an FNB statement
- Check PDF is text-based (not scanned image)

## Need Help?

The app runs locally on your computer:
- Your files stay private
- No internet connection needed (after installing)
- Files are deleted after conversion

---

**Enjoy OneShot Tools!** ⚡

For more details, see the full README.md

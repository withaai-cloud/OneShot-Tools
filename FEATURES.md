# OneShot Tools - Features & Specifications

## 🎯 Overview
OneShot Tools is a web-based productivity suite designed to simplify common business tasks. The application runs locally on your computer, ensuring data privacy and security.

## 📊 Bank Statement Converter

### Key Features

#### 1. Multi-File Upload
- Upload multiple PDF bank statements simultaneously
- Drag-and-drop interface for easy file selection
- Visual file list with file sizes
- Remove individual files before conversion

#### 2. Smart Extraction
- Automatically detects and extracts:
  - Transaction dates (DD/MM/YYYY format)
  - Transaction descriptions
  - Transaction amounts
- Handles various transaction types:
  - Credits (payments received)
  - Debits (payments made)
  - Fees and charges

#### 3. Amount Inversion Toggle
- One-click option to invert all amounts
- Useful for:
  - Reconciliation with different accounting systems
  - Reversing credit/debit conventions
  - Custom accounting requirements

#### 4. Batch Processing
For multiple files, you receive:
- **Individual Excel files** - One per PDF uploaded
- **Combined Excel file** - All transactions merged
- **ZIP archive** - Contains all generated files

#### 5. Excel Output Format
Generated spreadsheets include:
- **Date column**: DD/MM/YYYY format
- **Description column**: Full transaction details
- **Amount column**: Numerical values with proper formatting
  - Positive: Credits/Income
  - Negative: Debits/Expenses

### Technical Specifications

#### Supported Formats
- **Input**: PDF bank statements (FNB format)
- **Output**: Excel (.xlsx) spreadsheets

#### File Limits
- Maximum file size: 50MB per file
- No limit on number of files (within reasonable bounds)

#### Processing Speed
- Single file: ~2-5 seconds
- Multiple files: ~3-8 seconds per file
- Depends on file size and transaction count

## 🎨 User Interface

### Homepage
- Clean, modern design
- Tool cards with descriptions
- Feature highlights
- Easy navigation

### Converter Tool
- Intuitive upload interface
- Drag-and-drop support
- Real-time file list
- Clear options and controls
- Progress indicators
- Download links after conversion

## 🔒 Security & Privacy

### Data Handling
- All processing done locally on your computer
- No data sent to external servers
- Uploaded files temporarily stored during processing
- Files automatically deleted after conversion
- No data persistence or logging

### Recommended Use
- Local/internal network deployment
- Personal or business use
- Private data processing

## 🚀 Performance

### Optimization
- Efficient PDF text extraction
- Minimal memory footprint
- Quick conversion times
- Responsive user interface

### Scalability
- Handles statements with 100+ transactions
- Processes multiple files in parallel
- Works on standard computers (no special requirements)

## 📈 Future Enhancements

### Planned Features
1. **Additional Bank Formats**
   - Support for more banks (ABSA, Standard Bank, Nedbank, etc.)
   - International bank formats
   - Configurable extraction templates

2. **More Tools**
   - Invoice generator
   - Receipt organizer
   - Expense tracker
   - Document converter
   - Data merger

3. **Advanced Options**
   - Custom date formats
   - Category assignment
   - Transaction filtering
   - Custom column mapping
   - CSV output option

4. **Enhanced Features**
   - Transaction categorization
   - Duplicate detection
   - Balance reconciliation
   - Export to accounting software formats

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.13+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 100MB for application
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Recommended
- **RAM**: 4GB or more
- **Storage**: 1GB free space
- **Internet**: For initial setup (downloading dependencies)

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **pypdfium2**: PDF text extraction
- **openpyxl**: Excel file generation
- **Python 3**: Core language

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling (custom, no frameworks)
- **JavaScript**: Interactive functionality
- **No external dependencies**: Lightweight, fast loading

## 📦 Deployment Options

### Local Development
```bash
python app.py
```
Access at: http://localhost:5000

### Production Deployment
Options include:
- Docker container
- Virtual private server
- Internal company server
- Cloud hosting (AWS, Azure, Google Cloud)

### Network Access
- Can be configured for LAN access
- Suitable for team/department use
- Secure internal network deployment

## 🎓 Use Cases

### Individuals
- Personal finance management
- Tax preparation
- Expense tracking
- Budget planning

### Small Businesses
- Bookkeeping automation
- Transaction reconciliation
- Financial record keeping
- Audit preparation

### Accountants
- Client data processing
- Statement analysis
- Bulk transaction import
- Reconciliation workflows

### Finance Teams
- Department expense processing
- Multi-account reconciliation
- Financial reporting preparation
- Data consolidation

## 📄 License & Support

### License
MIT License - Free to use, modify, and distribute

### Support
- Documentation included
- Community support via GitHub (if published)
- Self-hosted solution (full control)

---

**OneShot Tools** - Making productivity simple, one tool at a time! ⚡

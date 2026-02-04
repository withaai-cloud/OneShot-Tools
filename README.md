# ⚡ OneShot Tools

A web-based productivity toolkit for business and personal use. Fast, simple, and powerful.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/oneshot-tools)

## ✨ Features

### 📊 Bank Statement Converter
Convert PDF bank statements to Excel spreadsheets with automatic data extraction.

- **Multi-file upload** - Process multiple statements at once
- **Smart extraction** - Automatically identifies dates, descriptions, and amounts
- **Amount inversion** - Toggle positive/negative values
- **Batch processing** - Get individual files plus combined output
- **Supports**: FNB bank statements

### 💰 SA Tax Split Optimizer
Calculate the optimal split between Individual and SBC tax structures to minimize tax liability.

- **2024/2025 tax rates** - Uses current South African tax brackets
- **Automatic optimization** - Tests thousands of combinations
- **Instant results** - See optimal split and savings immediately
- **Tax comparison** - Compare against single-structure taxation
- **Perfect for**: Small business owners, freelancers, tax planning

## 🎯 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/oneshot-tools.git
cd oneshot-tools

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

**Or use the startup scripts:**
- **Windows**: Double-click `start.bat`
- **Mac/Linux**: Run `bash start.sh`

### Deploy to Vercel

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

**Quick steps:**
1. Push this repository to GitHub
2. Sign up at [vercel.com](https://vercel.com)
3. Import your repository
4. Click Deploy
5. Done! 🎉

## 📋 Requirements

- Python 3.9+
- Flask 3.1.2
- pypdfium2 5.0.0
- openpyxl 3.1.5

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **PDF Processing**: pypdfium2
- **Excel Generation**: openpyxl
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Hosting**: Vercel-ready

## 📂 Project Structure

```
oneshot-tools/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html        # Homepage
│   ├── bank_statement_converter.html
│   └── tax_optimizer.html
├── static/
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── README.md            # This file
```

## 🔒 Privacy & Security

- All processing done server-side
- Files processed in temporary storage
- No data persistence or logging
- HTTPS encryption (when deployed)
- No user tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Adding New Tools

1. Create template in `templates/`
2. Add tool card to `index.html`
3. Add route in `app.py`
4. Add tool-specific JavaScript if needed

## 📝 License

MIT License - Free to use, modify, and distribute.

## 🌟 Roadmap

- [ ] Additional bank formats (ABSA, Standard Bank, Nedbank)
- [ ] Invoice generator
- [ ] Receipt organizer
- [ ] Expense tracker
- [ ] Document converter
- [ ] More tax calculators

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Deploy to Vercel, Railway, or Render
- [Quick Start Guide](QUICKSTART.md) - Get started in 3 steps
- [Features Documentation](FEATURES.md) - Detailed feature list

## 🙏 Acknowledgments

Built with Flask and love ❤️

---

**Made for productivity** ⚡

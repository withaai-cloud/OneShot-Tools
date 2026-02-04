#!/bin/bash

# OneShot Tools Startup Script

echo "========================================="
echo "   🚀 Starting OneShot Tools"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import flask, pypdfium2, openpyxl" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "📥 Installing required packages..."
    pip install flask pypdfium2 openpyxl
fi

echo ""
echo "✅ All dependencies ready!"
echo ""
echo "🌐 Starting web server..."
echo "   Access the app at: http://localhost:5000"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "========================================="
echo ""

# Start the Flask application
python3 app.py

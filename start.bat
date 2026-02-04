@echo off
REM OneShot Tools Startup Script for Windows

echo =========================================
echo    Starting OneShot Tools
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import flask, pypdfium2, openpyxl" >nul 2>&1

if errorlevel 1 (
    echo Installing required packages...
    pip install flask pypdfium2 openpyxl
)

echo.
echo All dependencies ready!
echo.
echo Starting web server...
echo Access the app at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo =========================================
echo.

REM Start the Flask application
python app.py

pause

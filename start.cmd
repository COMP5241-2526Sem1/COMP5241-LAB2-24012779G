@echo off
REM NoteTaker App Startup Script
REM This script activates the virtual environment and starts the Flask application

echo ========================================
echo    NoteTaker - Personal Note Manager
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run the following commands first:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Please ensure you're in the correct project directory.
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "src\main.py" (
    echo ERROR: src\main.py not found!
    echo Please ensure you're in the correct project directory.
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting NoteTaker application...
echo [INFO] Virtual environment: .venv
echo [INFO] Main script: src\main.py
echo [INFO] URL: http://localhost:5001
echo.

REM Activate virtual environment and start the app
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Checking dependencies...
pip install -r requirements.txt --quiet

echo [INFO] Starting Flask application...
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python src\main.py

REM If we reach here, the app has stopped
echo.
echo [INFO] NoteTaker application has stopped.
echo Press any key to exit...
pause >nul
@echo off
REM Setup Script for NoteTaker Application
echo ========================================
echo    NoteTaker - Initial Setup
echo ========================================
echo.

echo [INFO] Setting up Python virtual environment...
python -m venv .venv

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Installing required packages...
pip install -r requirements.txt

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo You can now start the application by running:
echo   start.cmd
echo.
echo Or by double-clicking the start.cmd file
echo.
pause
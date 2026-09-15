@echo off
title UGDS Patient Outreach Folder Watcher
cd /d "%~dp0"

echo ========================================================
echo   UGDS PATIENT OUTREACH FOLDER WATCHER
echo ========================================================
echo.

:: Check python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b
)

:: Install requirements if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo Starting Folder Watcher...
echo.
python watcher.py

pause

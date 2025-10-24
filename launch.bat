@echo off
REM Terminal Browser Navigator Launcher (Windows)

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo Setting up virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Installing Playwright browsers...
    playwright install chromium
) else (
    call venv\Scripts\activate.bat
)

REM Run the browser terminal
python browser_terminal.py

REM Keep terminal open
if errorlevel 1 (
    echo.
    echo Press any key to close...
    pause > nul
)

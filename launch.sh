#!/bin/bash
# Terminal Browser Navigator Launcher (Linux/Mac)

# Get the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the project directory
cd "$DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Installing Playwright browsers..."
    playwright install chromium
else
    source venv/bin/activate
fi

# Run the browser terminal
python3 browser_terminal.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press Enter to close..."
    read
fi

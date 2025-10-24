# Terminal Browser Navigator

Navigate the web through interactive terminal prompts - like a boot menu for your browser!

## 🚀 Features

- **Headless Browser Navigation**: Browse the web without opening a GUI browser
- **Interactive Prompts**: Boot menu-style interface for navigating pages
- **Auto-Detection**: Automatically detects links, buttons, and input fields on any page
- **Smart Controls**: Fill forms, click buttons, navigate links - all from your terminal
- **Beautiful UI**: Clean, colored terminal interface using Rich
- **Easy Launch**: Double-click launchers for Windows and Linux
- **Global Command**: Install as system-wide command - run from anywhere!
- **Split-Screen Mode**: Optional tmux integration for dual-pane browsing

## 📋 Requirements

- Python 3.8 or higher
- Internet connection
- Terminal/Command Prompt

## 🔧 Installation

### Quick Start (Auto-Install)

#### Linux/Mac:
```bash
# Simply double-click the launch.sh file in your file manager
# OR run from terminal:
./launch.sh
```

#### Windows:
```batch
REM Double-click launch.bat in File Explorer
REM OR run from Command Prompt:
launch.bat
```

The launcher will automatically:
1. Create a virtual environment
2. Install all dependencies
3. Download Chromium browser
4. Launch the application

### System-Wide Installation (Recommended)

Install once and run from anywhere in your terminal:

```bash
# Run the installer
./install.sh

# Choose installation method:
# 1. User installation (~/.local/bin)        - No sudo required
# 2. System-wide (/usr/local/bin)            - Requires sudo
# 3. Shell alias                             - Adds to .bashrc/.zshrc
# 4. Skip (use ./terminalbrowser directly)
```

After installation, you can run from any directory:

```bash
# Run normally
terminalbrowser

# Run with tmux split-screen mode
terminalbrowser --tmux

# Show help
terminalbrowser --help
```

**Tmux Split-Screen Mode:**
- Automatically splits your terminal into two panes
- Browser runs in one pane, info/status in the other
- Great for monitoring and multitasking
- Requires tmux: `sudo apt install tmux` (Linux) or `brew install tmux` (Mac)

### Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the application
python3 browser_terminal.py
```

## 🖱️ Desktop Integration

### Linux Desktop Shortcut

1. Open `TerminalBrowser.desktop` in a text editor
2. Replace `%{DIR}` with the full path to this directory
   ```
   Example: Exec=bash -c "cd '/home/username/terminalguiallos' && bash launch.sh"
   ```
3. Copy to Desktop or applications folder:
   ```bash
   # For Desktop icon:
   cp TerminalBrowser.desktop ~/Desktop/

   # For Applications menu:
   cp TerminalBrowser.desktop ~/.local/share/applications/
   ```
4. Make it executable:
   ```bash
   chmod +x ~/Desktop/TerminalBrowser.desktop
   ```
5. Right-click and select "Allow Launching" or "Trust and Launch"

### Windows Desktop Shortcut

1. Right-click on `launch.bat`
2. Select "Create shortcut"
3. Right-click the shortcut and select "Properties"
4. In "Run" dropdown, select "Minimized" or "Normal window"
5. Move the shortcut to your Desktop

## 🎮 Usage

### Starting the Browser

There are multiple ways to launch the browser:

**Method 1: Global Command (after running install.sh)**
```bash
terminalbrowser              # Launch normally
terminalbrowser --tmux       # Launch with split-screen
```

**Method 2: Double-Click Launcher**
- Linux/Mac: Double-click `launch.sh`
- Windows: Double-click `launch.bat`

**Method 3: Direct Script**
```bash
./terminalbrowser           # From project directory
python3 browser_terminal.py # Direct Python execution
```

Once launched:
1. Enter a starting URL (default: google.com)
2. Wait for the page to load
3. Start navigating with numbered options!

### Navigation Menu

The terminal will display:
- **Current Page Info**: Title and URL
- **Numbered Menu Options**:
  - `0`: Navigate to a specific URL
  - Input fields detected on the page (with field names)
  - Buttons you can click
  - Links you can follow

### Commands

- **Number (1-99)**: Select a menu option
- **0**: Go to a specific URL
- **r**: Refresh the current page
- **p**: Print page text content
- **q**: Quit the application

### Example Session

```
┌─────────────── Current Page ───────────────┐
│ Title: Google                              │
│ URL: https://www.google.com                │
└────────────────────────────────────────────┘

╭────┬──────────────────┬──────────────────────╮
│ #  │ Action           │ Description          │
├────┼──────────────────┼──────────────────────┤
│ 0  │ Go to URL        │ Navigate to URL      │
│ 1  │ Fill Input       │ [text] q - Search    │
│ 2  │ Click Button     │ Google Search        │
│ 3  │ Open Link        │ Gmail                │
│ 4  │ Open Link        │ Images               │
╰────┴──────────────────┴──────────────────────╯

Type 'q' to quit, 'r' to refresh, 'p' to print

Select option: 1
Enter q: python tutorials
Select option: 2
[Clicking Google Search button]
```

## 🌐 What You Can Do

- **Search Engines**: Navigate Google, Bing, DuckDuckGo with ease
- **Read Articles**: Browse news sites, blogs, documentation
- **Fill Forms**: Enter search queries, login forms, contact forms
- **Browse Catalogs**: Navigate e-commerce sites, directories
- **Research**: Follow links, read content, explore topics

## 🛠️ How It Works

1. **Headless Browser**: Runs Chromium in headless mode (no GUI)
2. **Page Analysis**: Extracts interactive elements (links, buttons, inputs)
3. **Menu Generation**: Creates numbered options for each element
4. **User Selection**: You choose actions via prompts
5. **Action Execution**: Executes your choice on the headless browser
6. **Loop**: Repeats for the next page

## 📁 Project Structure

```
terminalguiallos/
├── browser_terminal.py     # Main application
├── requirements.txt        # Python dependencies
├── launch.sh              # Linux/Mac launcher
├── launch.bat             # Windows launcher
├── TerminalBrowser.desktop # Linux desktop entry
├── README.md              # This file
└── venv/                  # Virtual environment (created on first run)
```

## 🐛 Troubleshooting

### "python3: command not found"
- Install Python from python.org
- On Windows, use `python` instead of `python3`

### "playwright install failed"
- Run manually: `venv/bin/playwright install chromium`
- Ensure you have internet connection

### "Permission denied" on Linux
- Make scripts executable: `chmod +x launch.sh`

### Elements not detected
- Some sites use JavaScript-heavy content
- Try pressing 'r' to refresh after the page loads
- Use 'p' to see page content

### Launcher doesn't open terminal
- On Linux, ensure desktop file has correct path
- Right-click and check "Trust and Launch" or "Allow Executing"

## 🔒 Privacy & Security

- All browsing is local on your machine
- No data is sent anywhere except normal web requests
- Headless browser runs with same permissions as regular browser
- No history or cookies are saved between sessions

## 🤝 Contributing

Feel free to enhance this project! Some ideas:
- Add bookmark management
- Implement tab/window management
- Add screenshot capability
- Create history tracking
- Add configuration file for settings

## 📝 License

This project is open source and available under the MIT License.

## 💡 Tips

- Start with simple sites like Google or Wikipedia
- Use specific URLs (include https://)
- Some complex web apps may not work well in headless mode
- Single-page apps (SPAs) might need page refresh ('r') to see updates
- Use 'p' command to read article content in terminal

---

**Enjoy browsing the web from your terminal! 🖥️✨**

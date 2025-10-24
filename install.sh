#!/bin/bash
# Terminal Browser Navigator - System Installation Script
# This script installs the browser as a global command

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the absolute path to this directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Terminal Browser Navigator Installer  ║${NC}"
echo -e "${CYAN}╔════════════════════════════════════════╝${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$INSTALL_DIR/venv"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate and install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
source "$INSTALL_DIR/venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$INSTALL_DIR/requirements.txt"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install Playwright browsers
echo -e "${YELLOW}Installing Chromium browser...${NC}"
playwright install chromium
echo -e "${GREEN}✓ Chromium installed${NC}"

# Create wrapper script
WRAPPER_SCRIPT="$INSTALL_DIR/terminalbrowser"
cat > "$WRAPPER_SCRIPT" << 'WRAPPER_EOF'
#!/bin/bash
# Terminal Browser Navigator - Global Command Wrapper

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment and run
source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/browser_terminal.py" "$@"
WRAPPER_EOF

chmod +x "$WRAPPER_SCRIPT"
echo -e "${GREEN}✓ Wrapper script created${NC}"

# Determine installation method
echo ""
echo -e "${CYAN}Choose installation method:${NC}"
echo "1) Install for current user only (~/.local/bin)"
echo "2) Install system-wide (/usr/local/bin) [requires sudo]"
echo "3) Add alias to shell config (no copying)"
echo "4) Skip global installation (use ./terminalbrowser)"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        # Install to ~/.local/bin
        BIN_DIR="$HOME/.local/bin"
        mkdir -p "$BIN_DIR"
        ln -sf "$WRAPPER_SCRIPT" "$BIN_DIR/terminalbrowser"
        echo -e "${GREEN}✓ Installed to $BIN_DIR/terminalbrowser${NC}"

        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
            echo ""
            echo -e "${YELLOW}⚠ Warning: $BIN_DIR is not in your PATH${NC}"
            echo -e "${CYAN}Add this line to your ~/.bashrc or ~/.zshrc:${NC}"
            echo -e "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            echo "After adding, run: source ~/.bashrc (or ~/.zshrc)"
        fi
        ;;
    2)
        # Install system-wide
        sudo ln -sf "$WRAPPER_SCRIPT" /usr/local/bin/terminalbrowser
        echo -e "${GREEN}✓ Installed to /usr/local/bin/terminalbrowser${NC}"
        ;;
    3)
        # Add alias
        SHELL_RC=""
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        fi

        if [ -n "$SHELL_RC" ]; then
            ALIAS_LINE="alias terminalbrowser='$WRAPPER_SCRIPT'"
            if ! grep -q "alias terminalbrowser=" "$SHELL_RC" 2>/dev/null; then
                echo "" >> "$SHELL_RC"
                echo "# Terminal Browser Navigator" >> "$SHELL_RC"
                echo "$ALIAS_LINE" >> "$SHELL_RC"
                echo -e "${GREEN}✓ Alias added to $SHELL_RC${NC}"
                echo -e "${CYAN}Run: source $SHELL_RC${NC}"
            else
                echo -e "${YELLOW}⚠ Alias already exists in $SHELL_RC${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ Could not detect shell config file${NC}"
            echo -e "${CYAN}Add this to your shell config:${NC}"
            echo -e "  alias terminalbrowser='$WRAPPER_SCRIPT'"
        fi
        ;;
    4)
        echo -e "${CYAN}ℹ No global installation. Run with: $WRAPPER_SCRIPT${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Installation Complete!          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Usage:${NC}"
if [ "$choice" != "4" ]; then
    echo -e "  ${GREEN}terminalbrowser${NC}      - Launch the browser"
else
    echo -e "  ${GREEN}./terminalbrowser${NC}    - Launch the browser"
fi
echo ""
echo -e "${CYAN}Optional: For split-screen mode with tmux, run:${NC}"
echo -e "  ${GREEN}terminalbrowser --tmux${NC}"
echo ""

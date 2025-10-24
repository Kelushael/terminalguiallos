#!/usr/bin/env python3
"""
Terminal-based Web Browser Navigator
Navigate websites through interactive terminal prompts
"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from bs4 import BeautifulSoup
import sys
import os
import subprocess
import argparse
from typing import List, Dict, Optional
import re


class BrowserNavigator:
    def __init__(self):
        self.console = Console()
        self.page: Optional[Page] = None
        self.browser: Optional[Browser] = None
        self.playwright = None
        self.history = []

    async def initialize(self):
        """Initialize the headless browser"""
        self.console.print(Panel.fit(
            "[bold cyan]Terminal Browser Navigator[/bold cyan]\n"
            "Initializing headless browser...",
            border_style="cyan"
        ))

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

        self.console.print("[green]✓ Browser ready![/green]\n")

    async def analyze_page(self) -> Dict:
        """Analyze the current page and extract interactive elements"""
        content = await self.page.content()
        soup = BeautifulSoup(content, 'lxml')

        # Get page info
        title = await self.page.title()
        url = self.page.url

        # Extract interactive elements
        links = []
        buttons = []
        inputs = []

        # Get links (limit to most relevant)
        for link in soup.find_all('a', href=True)[:20]:
            text = link.get_text(strip=True)
            href = link.get('href')
            if text and href and not href.startswith('#'):
                links.append({'text': text[:60], 'href': href})

        # Get buttons
        for button in soup.find_all('button')[:10]:
            text = button.get_text(strip=True)
            if text:
                buttons.append({'text': text[:60], 'selector': button.name})

        # Get input fields
        for input_field in soup.find_all('input')[:10]:
            input_type = input_field.get('type', 'text')
            placeholder = input_field.get('placeholder', '')
            name = input_field.get('name', input_field.get('id', ''))
            if input_type not in ['hidden', 'submit']:
                inputs.append({
                    'type': input_type,
                    'name': name,
                    'placeholder': placeholder[:40]
                })

        return {
            'title': title,
            'url': url,
            'links': links,
            'buttons': buttons,
            'inputs': inputs
        }

    def display_page_info(self, page_data: Dict):
        """Display current page information"""
        self.console.clear()

        # Header
        header = Table.grid(padding=(0, 2))
        header.add_column(style="cyan", justify="left")
        header.add_row(f"[bold]Title:[/bold] {page_data['title']}")
        header.add_row(f"[bold]URL:[/bold] {page_data['url']}")

        self.console.print(Panel(header, title="[bold cyan]Current Page[/bold cyan]", border_style="cyan"))
        self.console.print()

    def display_menu(self, page_data: Dict) -> List[Dict]:
        """Display interactive menu and return options"""
        options = []
        option_num = 1

        menu_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        menu_table.add_column("#", style="cyan", width=4)
        menu_table.add_column("Action", style="green")
        menu_table.add_column("Description", style="white")

        # Navigation options
        menu_table.add_row("0", "[yellow]Go to URL[/yellow]", "Navigate to a specific URL")
        options.append({'type': 'navigate', 'action': 'go_to_url'})

        # Back option
        if len(self.history) > 1:
            menu_table.add_row(str(option_num), "[yellow]Back[/yellow]", "Go back to previous page")
            options.append({'type': 'navigate', 'action': 'back'})
            option_num += 1

        # Input fields
        if page_data['inputs']:
            self.console.print("[bold]Input Fields:[/bold]")
            for inp in page_data['inputs']:
                desc = f"[{inp['type']}] {inp['name']}"
                if inp['placeholder']:
                    desc += f" - {inp['placeholder']}"
                menu_table.add_row(str(option_num), f"[blue]Fill Input[/blue]", desc)
                options.append({'type': 'input', 'data': inp})
                option_num += 1

        # Buttons
        if page_data['buttons']:
            for btn in page_data['buttons'][:5]:
                menu_table.add_row(str(option_num), f"[green]Click Button[/green]", btn['text'])
                options.append({'type': 'button', 'data': btn})
                option_num += 1

        # Links
        if page_data['links']:
            self.console.print()
            for i, link in enumerate(page_data['links'][:15], option_num):
                menu_table.add_row(str(i), f"[cyan]Open Link[/cyan]", link['text'])
                options.append({'type': 'link', 'data': link})

        self.console.print(menu_table)
        self.console.print()

        # Additional options
        self.console.print("[dim]Type 'q' to quit, 'r' to refresh, 'p' to print page content[/dim]")
        self.console.print()

        return options

    async def navigate_to(self, url: str):
        """Navigate to a URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        self.console.print(f"[yellow]Navigating to {url}...[/yellow]")
        try:
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            self.history.append(url)
            self.console.print("[green]✓ Page loaded[/green]")
            await asyncio.sleep(1)
        except Exception as e:
            self.console.print(f"[red]✗ Error loading page: {e}[/red]")
            await asyncio.sleep(2)

    async def fill_input(self, input_data: Dict):
        """Fill an input field"""
        self.console.print(f"[cyan]Filling input: {input_data['name']}[/cyan]")

        if input_data['type'] == 'password':
            value = Prompt.ask(f"Enter {input_data['name']}", password=True)
        else:
            value = Prompt.ask(f"Enter {input_data['name']}")

        try:
            # Try multiple selector strategies
            selectors = [
                f"input[name='{input_data['name']}']",
                f"input[id='{input_data['name']}']",
                f"input[placeholder*='{input_data['placeholder']}']"
            ]

            filled = False
            for selector in selectors:
                try:
                    await self.page.fill(selector, value, timeout=2000)
                    self.console.print("[green]✓ Input filled[/green]")
                    filled = True
                    break
                except:
                    continue

            if not filled:
                self.console.print("[red]✗ Could not find input field[/red]")

            await asyncio.sleep(1)
        except Exception as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            await asyncio.sleep(2)

    async def click_button(self, button_data: Dict):
        """Click a button"""
        self.console.print(f"[green]Clicking button: {button_data['text']}[/green]")

        try:
            # Try to find and click the button by text
            await self.page.get_by_role("button", name=re.compile(button_data['text'], re.IGNORECASE)).first.click(timeout=5000)
            self.console.print("[green]✓ Button clicked[/green]")
            await asyncio.sleep(2)
        except Exception as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            await asyncio.sleep(2)

    async def click_link(self, link_data: Dict):
        """Click a link"""
        self.console.print(f"[cyan]Opening link: {link_data['text']}[/cyan]")

        try:
            # Handle relative URLs
            if link_data['href'].startswith('http'):
                url = link_data['href']
            elif link_data['href'].startswith('/'):
                current_url = self.page.url
                base_url = '/'.join(current_url.split('/')[:3])
                url = base_url + link_data['href']
            else:
                url = link_data['href']

            await self.navigate_to(url)
        except Exception as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            await asyncio.sleep(2)

    async def print_page_content(self):
        """Print readable page content"""
        content = await self.page.content()
        soup = BeautifulSoup(content, 'lxml')

        # Extract text content
        text = soup.get_text(separator='\n', strip=True)
        lines = [line for line in text.split('\n') if line.strip()]

        self.console.print(Panel('\n'.join(lines[:50]), title="Page Content (first 50 lines)", border_style="blue"))
        Prompt.ask("\nPress Enter to continue")

    async def run(self):
        """Main run loop"""
        await self.initialize()

        # Start with a homepage
        start_url = Prompt.ask(
            "[bold cyan]Enter starting URL[/bold cyan]",
            default="google.com"
        )
        await self.navigate_to(start_url)

        # Main loop
        while True:
            try:
                # Analyze current page
                page_data = await self.analyze_page()

                # Display page info and menu
                self.display_page_info(page_data)
                options = self.display_menu(page_data)

                # Get user choice
                choice = Prompt.ask("[bold yellow]Select option[/bold yellow]")

                # Handle special commands
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'r':
                    await self.page.reload()
                    continue
                elif choice.lower() == 'p':
                    await self.print_page_content()
                    continue
                elif choice == '0':
                    url = Prompt.ask("Enter URL")
                    await self.navigate_to(url)
                    continue

                # Handle numbered options
                try:
                    choice_idx = int(choice) - 1
                    if choice_idx < 0 or choice_idx >= len(options):
                        self.console.print("[red]Invalid option[/red]")
                        await asyncio.sleep(1)
                        continue

                    option = options[choice_idx]

                    if option['type'] == 'navigate':
                        if option['action'] == 'back':
                            await self.page.go_back()
                            await asyncio.sleep(1)
                    elif option['type'] == 'input':
                        await self.fill_input(option['data'])
                    elif option['type'] == 'button':
                        await self.click_button(option['data'])
                    elif option['type'] == 'link':
                        await self.click_link(option['data'])

                except ValueError:
                    self.console.print("[red]Invalid input[/red]")
                    await asyncio.sleep(1)

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                await asyncio.sleep(2)

        # Cleanup
        self.console.print("\n[yellow]Closing browser...[/yellow]")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        self.console.print("[green]Goodbye![/green]")


def check_tmux():
    """Check if running inside tmux"""
    return os.environ.get('TMUX') is not None


def launch_with_tmux():
    """Launch the application in a tmux split"""
    if check_tmux():
        # Already in tmux, create a split
        print("Creating tmux split pane...")
        # Split horizontally (top/bottom)
        subprocess.run(['tmux', 'split-window', '-v', '-p', '70',
                       f'python3 {os.path.abspath(__file__)}'])
        print("Browser launched in split pane!")
        print("Use Ctrl+B then arrow keys to switch between panes")
        print("Press Enter to close this message...")
        input()
    else:
        # Not in tmux, start a new tmux session with split
        print("Starting new tmux session with split view...")
        script_path = os.path.abspath(__file__)

        # Create a tmux session with a split
        tmux_commands = f"""
            tmux new-session -d -s terminalbrowser
            tmux split-window -v -p 70 -t terminalbrowser 'python3 {script_path}'
            tmux select-pane -t 0
            tmux send-keys -t terminalbrowser:0.0 'echo "Terminal Browser Navigator - Info Pane"' C-m
            tmux send-keys -t terminalbrowser:0.0 'echo ""' C-m
            tmux send-keys -t terminalbrowser:0.0 'echo "Browser running in bottom pane"' C-m
            tmux send-keys -t terminalbrowser:0.0 'echo "Ctrl+B then arrow keys to switch panes"' C-m
            tmux send-keys -t terminalbrowser:0.0 'echo "Type \\"exit\\" or Ctrl+D to close this pane"' C-m
            tmux attach-session -t terminalbrowser
        """

        subprocess.run(['bash', '-c', tmux_commands.strip()])


async def main(args):
    """Main entry point with argument support"""
    navigator = BrowserNavigator()
    await navigator.run()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Terminal Browser Navigator - Browse the web from your terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  terminalbrowser                  # Launch normally
  terminalbrowser --tmux          # Launch with tmux split view
  terminalbrowser --help          # Show this help message

Controls:
  0-99  : Select menu option
  0     : Go to URL
  r     : Refresh page
  p     : Print page content
  q     : Quit
        """
    )

    parser.add_argument(
        '--tmux',
        action='store_true',
        help='Launch in tmux split-screen mode'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Terminal Browser Navigator v1.0'
    )

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()

        if args.tmux:
            # Check if tmux is installed
            if subprocess.run(['which', 'tmux'], capture_output=True).returncode != 0:
                print("Error: tmux is not installed.")
                print("Install it with: sudo apt install tmux  (Ubuntu/Debian)")
                print("              or: brew install tmux      (Mac)")
                sys.exit(1)

            launch_with_tmux()
        else:
            asyncio.run(main(args))

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

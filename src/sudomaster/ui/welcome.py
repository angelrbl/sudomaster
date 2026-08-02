from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.align import Align

console = Console()

UI_WIDTH = 80

ASCII_BANNER = r"""
  ___  _   _ ___   ___  __  __   _   ___ _____ _____ ___ 
 / __|| | | |   \ / _ \|  \/  | /_\ / __|_   _| ___| _ \
 \__ \| |_| | |) | (_) | |\/| |/ _ \\__ \ | | | _| |   /
 |___/ \___/|___/ \___/|_|  |_/_/ \_\___/ |_| |___|_|_\ 
"""

def render_welcome_screen() -> None:
    banner_aligned = Align.center(f"[bold yellow]{ASCII_BANNER.strip("\n")}[/bold yellow]")

    subtitle_panel = (Panel(
        Align.center("[italic]The Ultimate Sudoku Solver Engine & Performance Analytics CLI[/italic]"),
        title="[bold yellow]Sudomaster CLI[/bold yellow]",
        width=UI_WIDTH
    ))

    table = Table(title="\n[bold yellow]Available commands[/bold yellow]", show_header=True, header_style="bold yellow", width=UI_WIDTH)
    table.add_column("Command", style="bold white")
    table.add_column("Description", style="bold white")

    table.add_row("sudomaster generate", "Generates a new Sudoku with the selected difficulty")
    table.add_row("sudomaster solve", "Solves a given Sudoku with the specified solver")
    table.add_row("sudomaster benchmark", "Runs a benchmark from a specific solver and difficulty")
    table.add_row("sudomaster plot", "Visualize advanced metrics from a benchmark file")

    footer = "\n[dim]Use [bold]sudomaster <command> --help[/bold] to see command's specific options.[/dim]\n"

    console.print(banner_aligned)
    console.print()
    console.print(Align.center(subtitle_panel))
    console.print(Align.center(table))
    console.print()
    console.print(Align.center(footer))
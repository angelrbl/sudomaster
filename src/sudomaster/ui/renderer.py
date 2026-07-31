from rich.text import Text
from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich import box
from sudomaster.core import Board

def build_board_table(board: Board, title: str = "Sudoku") -> Table:
    table = Table(
        show_header=False,
        box=box.ROUNDED,
        show_lines=True,
        title=f"[bold cyan]{title}[/bold cyan]",
        padding=(0, 1)
    )

    for _ in range(board.cols):
        table.add_column(justify="center")

    for r in range(board.rows):
        row_text_values = []
        for c in range(board.cols):
            is_alternate_block = ((r // 3) + (c // 3)) % 2 == 0
            val = board.get(row=r, col=c)
            row_text_values.append(Text(text=f"{str(val) if val != 0 else ""}", style=f"bold {"white" if is_alternate_block is True else "yellow"}"))
        table.add_row(*row_text_values)

    return table

def print_board(board: Board, title: str = "Sudoku", console: Console | None = None) -> None:
    if console is None:
        console = Console()

    table = build_board_table(board=board, title=title)

    console.print(table)

def print_boards(boards: list[Board], titles: list[str] | None = None, console: Console | None = None) -> None:
    if console is None:
        console = Console()

    tables = []
    for i, board in enumerate(boards):
        table_title = titles[i] if titles and i < len(titles) else None
        tables.append(build_board_table(board=board, title=table_title))

    console.print(Columns(tables, padding=(1, 2)))

if __name__ == "__main__":
    from sudomaster.core import SudokuGenerator
    generator = SudokuGenerator()
    result = generator.generate()
    
    print_board(board=result.sudoku, title="Sudoku")
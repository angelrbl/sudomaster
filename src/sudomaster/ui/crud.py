import click
from pathlib import Path
from rich.prompt import Prompt

from sudomaster.core import SudokuGenerator, Difficulty, board_to_string
from sudomaster.io import save_data, resolve_output_path, UnsupportedFileFormatException
from sudomaster.ui import print_board, print_boards

@click.command()
@click.option("--difficulty", "-d", type=click.Choice(["easy", "medium", "hard"], case_sensitive=False), help="Choose sudoku's difficulty.")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    is_flag=False,
    flag_value="AUTO",
    help="Output path (i.e. ./results/sudoku_easy_1.json)")
@click.option("--raw", "-r", is_flag=True, help="Return sudoku as string.")
@click.option("--seed", type=int, help="Specify the generator's seed.")
@click.option("--solution", "-s", is_flag=True, help="Return/export sudoku's solution.")
def generate(difficulty, output, raw, seed, solution):
    """Generates a new Sudoku with the selected difficulty"""

    if not difficulty:
        difficulty = Prompt.ask(prompt="Select the difficulty of your sudoku", choices=["easy", "medium", "hard"], case_sensitive=False)

    generator = SudokuGenerator(seed=seed)
    result = generator.generate(difficulty=Difficulty[difficulty.upper()])

    if output:
        if not Path(output).suffix:
            ext = Prompt.ask(prompt="Select an exporting format for your sudoku", choices=["json", "csv", "txt"], case_sensitive=False)
        else:
            ext = Path(output).suffix.lstrip(".").lower()
        final_path = resolve_output_path(output_arg=output, difficulty=difficulty, ext=ext, seed=seed)
        try:
            save_data(obj=result, filepath=final_path)
            click.echo(f"\nSudoku saved successfully at: {final_path}")
        except UnsupportedFileFormatException as e:
            raise click.ClickException(str(e))

    if raw:
        board_string = board_to_string(board=(result.solution if solution else result.sudoku))
        click.echo(board_string)
    else:
        click.echo("\n")
        if not solution:
            print_board(result.sudoku, title="Generated Sudoku")
        else:
            print_boards(boards=[result.sudoku, result.solution], titles=["Generated Sudoku", "Solution"])

@click.command()
def solve():
    print("I'm solving a sudoku")

@click.command()
def benchmark():
    print("I'm running a benchmark")
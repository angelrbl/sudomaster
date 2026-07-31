import click
from pathlib import Path
from rich.prompt import Prompt

from sudomaster.core import SudokuGenerator, Difficulty, board_to_string, parse_board_string, Board, GeneratedSudoku
from sudomaster.solvers import SolverResult, BacktrackingSolver
from sudomaster.io import load_data, save_data, resolve_output_path, UnsupportedFileFormatException
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
        final_path = resolve_output_path(output_arg=output, difficulty_or_solved=difficulty, ext=ext, seed=seed)
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
@click.option("--file", "-f", type=click.Path(exists=True, file_okay=True, dir_okay=False), help="Input file where the sudoku to solve is.")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    is_flag=False,
    flag_value="AUTO",
    help="Output path (i.e. ./results/sudoku_easy_1.json)")
@click.option("--raw", "-r", is_flag=True, help="Return sudoku as string.")
@click.option("--solver", "-s", type=click.Choice(["backtracking"], case_sensitive=False), help="Specify the solver that solves the sudoku.")
def solve(file, output, raw, solver):
    SOLVER_MAP = {
        "backtracking": BacktrackingSolver,
    }

    if not solver:
        solver = Prompt.ask(prompt="Select which solver will solve the sudoku", choices=["backtracking"], case_sensitive=False)

    if file:
        loaded_data = load_data(filepath=file)
        match loaded_data:
            case Board():
                sudoku_to_solve = loaded_data
            case GeneratedSudoku():
                sudoku_to_solve = loaded_data.sudoku
            case SolverResult():
                sudoku_to_solve = loaded_data.board
            case _:
                raise click.ClickException("The file does not contain a supported type")
    else:
        board_string = Prompt.ask(prompt="Introduce a sudoku string")
        try:
            sudoku_to_solve = parse_board_string(board_string=board_string)
        except ValueError as e:
            raise click.ClickException(f"Introduced sudoku string is not valid: '{e}'")

    if sudoku_to_solve.is_solved():
        raise click.ClickException("This sudoku is already solved.")
    
    solver_instance = SOLVER_MAP[solver.lower()]()
    result = solver_instance.solve(board=sudoku_to_solve)

    if result.success is False:
        raise click.ClickException("The sudoku does not have a solution.")

    if output:
            if not Path(output).suffix:
                ext = Prompt.ask(prompt="Select an exporting format for your sudoku", choices=["json", "csv", "txt"], case_sensitive=False)
            else:
                ext = Path(output).suffix.lstrip(".").lower()
            final_path = resolve_output_path(output_arg=output, difficulty_or_solved="solved", ext=ext)
            try:
                save_data(obj=result, filepath=final_path)
                click.echo(f"\nSudoku saved successfully at: {final_path}")
            except UnsupportedFileFormatException as e:
                raise click.ClickException(str(e))
    
    if raw:
        board_string = board_to_string(board=(result.board))
        click.echo(board_string)
    else:
        click.echo(f"\nSuccessfully solved the sudoku in {result.execution_time}s. Showing solution:\n")
        print_boards(
            boards=[sudoku_to_solve, result.board], 
            titles=["Original Sudoku", "Solved Sudoku"]
        )
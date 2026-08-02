import click
from pathlib import Path
from rich.prompt import Prompt
import pandas as pd

from sudomaster.core import SudokuGenerator, Difficulty, board_to_string, parse_board_string, Board, GeneratedSudoku
from sudomaster.solvers import SolverResult, BacktrackingSolver
from sudomaster.io import load_data, save_data, resolve_output_path, UnsupportedFileFormatException
from sudomaster.ui import print_board, print_boards
from sudomaster.ui.charts import render_benchmark_charts, plot_scatter_backtracks_vs_time, plot_time_distribution
from sudomaster.analytics import run_benchmark, benchmark_to_dataframe, get_summary_dataframe

SOLVER_MAP = {
        "backtracking": BacktrackingSolver,
}

@click.command()
@click.option("--difficulty", "-d", type=click.Choice(["easy", "medium", "hard", "expert", "master"], case_sensitive=False), help="Choose sudoku's difficulty.")
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
def generate(difficulty: str, output: Path | str, raw: bool, seed: int | None, solution: bool) -> None:
    """Generates a new Sudoku with the selected difficulty"""

    if not difficulty:
        difficulty = Prompt.ask(prompt="Select the difficulty of your sudoku", choices=["easy", "medium", "hard", "expert", "master"], case_sensitive=False)

    generator = SudokuGenerator(seed=seed)
    result = generator.generate(difficulty=Difficulty[difficulty.upper()])

    if output:
        if not Path(output).suffix:
            ext = Prompt.ask(prompt="Select an exporting format for your sudoku", choices=["json", "csv", "txt"], case_sensitive=False)
        else:
            ext = Path(output).suffix.lstrip(".").lower()
        final_path = resolve_output_path(output_arg=output, ext=ext, default_name=f"sudoku_{difficulty}", seed=seed)
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
    help="Output path (i.e. ./results/solved_sudoku_1.json)")
@click.option("--raw", "-r", is_flag=True, help="Return sudoku as string.")
@click.option("--solver", "-s", type=click.Choice(["backtracking"], case_sensitive=False), help="Specify the solver that solves the sudoku.")
def solve(file: Path | str, output: Path | str, raw: bool, solver: str) -> None:
    """Solves a given Sudoku with the specified solver."""

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
            final_path = resolve_output_path(output_arg=output, ext=ext, default_name=f"solved_sudoku")
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

@click.command()
@click.option("--solver", "-s", type=click.Choice(["backtracking"], case_sensitive=False), help="Specify the solver that the benchmark uses.")
@click.option("--difficulty", "-d", type=click.Choice(["easy", "medium", "hard", "expert", "master", "all"], case_sensitive=False), help="Choose sudoku's difficulty.")
@click.option("--samples", "-n", type=int, help="Number of sudokus generated by the benchmark.")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    is_flag=False,
    flag_value="AUTO",
    help="Output path (i.e. ./results/benchmarks/benchmark_backtracking_medium_1.csv)")
@click.option("--chart", "-c", is_flag=True, help="Print benchmark's charts")
def benchmark(solver: str, difficulty: str, samples: int, output: Path | str, chart: bool) -> None:
    """Runs a benchmark from a specific solver and difficulty."""

    if not difficulty:
        difficulty = Prompt.ask(prompt="Select the difficulty of your sudoku", choices=["easy", "medium", "hard", "expert", "master", "all"], case_sensitive=False)

    if not solver:
        solver = Prompt.ask(prompt="Select which solver will solve the sudoku", choices=["backtracking"], case_sensitive=False)
    solver_instance = SOLVER_MAP[solver.lower()]()

    with click.progressbar(
        length=samples,
        label=f"Running {samples} tests ({difficulty})..."
    ) as bar:
        
        benchmark_results = run_benchmark(
            solver_name=solver,
            solver=solver_instance,
            difficulty=(Difficulty[difficulty.upper()] if difficulty != "all" else None),
            samples=samples,
            on_progress=lambda: bar.update(1)
        )

    results_df = benchmark_to_dataframe(benchmark_results)

    if output:
        if not Path(output).suffix:
            ext = "csv"
        else:
            ext = Path(output).suffix.lstrip(".").lower()
        final_path = resolve_output_path(output_arg=output, ext=ext, default_dir=Path("./results/benchmarks/"), default_name=f"benchmark_solver_{difficulty}")
        try:
            save_data(obj=results_df, filepath=final_path)
            click.echo(f"\nBenchmark saved successfully at: {final_path}")
        except UnsupportedFileFormatException as e:
            raise click.ClickException(str(e))

    click.echo("\n")
    click.echo(get_summary_dataframe(df=results_df))

    if chart:
        render_benchmark_charts(df=results_df)

@click.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option(
    "--type",
    "-t",
    type=click.Choice(["summary", "scatter", "dist"], case_sensitive=False),
    help="Type of chart: 'summary' (bars), 'scatter' (points), or 'dist' (histogram).",
)
def plot(filepath: str | Path, type: str | None) -> None:
    """Visualize benchmark metrics from a saved CSV file."""

    if not type:
        type = Prompt.ask(prompt="Select a metric to visualize", choices=["summary", "scatter", "dist"], case_sensitive=False)

    try:
        df = load_data(filepath=filepath, target_class=pd.DataFrame)

        if df.empty:
            click.echo("WARNING: The CSV contains no data.")

        match type:
            case "summary":
                render_benchmark_charts(df=df)
            case "scatter":
                plot_scatter_backtracks_vs_time(df=df)
            case "dist":
                plot_time_distribution(df=df)
    except Exception as e:
        from rich.console import Console
        Console().print_exception(show_locals=True)
        raise click.ClickException(f"Error loading benchmark file: '{e}'")
import click
from pathlib import Path
from rich.prompt import Prompt
from sudomaster.core import Difficulty, SudokuGenerator

@click.command()
@click.option("--difficulty", "-d", type=click.Choice(["easy", "medium", "hard"]), help="Choose sudoku's difficulty.")
@click.option("--output", "-o", type=click.Path(), help="Output path (i.e. ./results/sudoku_easy_1.json)")
@click.option("--raw", "-r", is_flag=True, help="Return sudoku as string.")
@click.option("--seed", type=int, help="Specify the generator's seed.")
@click.option("--solution", "-s", is_flag=True, help="Return/export sudoku's solution.")
def generate(difficulty, output, raw, seed, solution):
    if not difficulty:
        difficulty = Prompt.ask(prompt="Select the difficulty of your sudoku", choices=["easy", "medium", "hard"])

    generator = SudokuGenerator(seed=seed)
    result = generator.generate(difficulty=Difficulty[difficulty.upper()])

    if solution:
        click.echo(result.solution)
    else:
        click.echo(result.sudoku)

@click.command()
def solve():
    print("I'm solving a sudoku")

@click.command()
def benchmark():
    print("I'm running a benchmark")
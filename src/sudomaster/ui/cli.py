import click
from sudomaster.ui.crud import generate, solve, benchmark

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("I'm working!")

cli.add_command(generate)
cli.add_command(solve)
cli.add_command(benchmark)
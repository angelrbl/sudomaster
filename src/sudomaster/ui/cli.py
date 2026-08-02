import click
from sudomaster.ui.crud import generate, solve, benchmark, plot
from sudomaster.ui.welcome import render_welcome_screen

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        render_welcome_screen()

cli.add_command(generate)
cli.add_command(solve)
cli.add_command(benchmark)
cli.add_command(plot)
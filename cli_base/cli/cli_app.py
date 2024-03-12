"""
    CLI for usage
"""
import logging
import sys

import rich_click as click
from rich import print  # noqa
from rich.console import Console
from rich.traceback import install as rich_traceback_install
from rich_click import RichGroup

import cli_base
from cli_base import constants
from cli_base.cli_tools import git_history
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from cli_base.cli_tools.version_info import print_version


logger = logging.getLogger(__name__)


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


######################################################################################################


@cli.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def update_readme_history(verbosity: int):
    """
    Update project history base on git commits/tags in README.md

    Will be exited with 1 if the README.md was updated otherwise with 0.

    Also, callable via e.g.:
        python -m cli_base update-readme-history -v
    """
    setup_logging(verbosity=verbosity)
    updated = git_history.update_readme_history(verbosity=verbosity)
    exit_code = 1 if updated else 0
    if verbosity:
        print(f'{exit_code=}')
    sys.exit(exit_code)


######################################################################################################


def main():
    print_version(cli_base)

    console = Console()
    rich_traceback_install(
        width=console.size.width,  # full terminal width
        show_locals=True,
        suppress=[click],
        max_frames=2,
    )

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()

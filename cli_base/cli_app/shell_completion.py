import logging

from rich import print  # noqa

from cli_base.cli_app import app
from cli_base.cli_tools.shell_completion import setup_tyro_shell_completion
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType


logger = logging.getLogger(__name__)


@app.command
def shell_completion(verbosity: TyroVerbosityArgType = 1, remove: bool = False) -> None:
    """
    Setup shell completion for this CLI (Currently only for bash and zsh)
    """
    setup_logging(verbosity=verbosity)
    setup_tyro_shell_completion(
        prog_name='cli_base_utilities_app_cli',
        remove=remove,
    )

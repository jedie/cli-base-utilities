import logging
import sys
from pathlib import Path

from rich import print  # noqa

from cli_base.cli_app import app
from cli_base.cli_tools import git_history
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType


logger = logging.getLogger(__name__)


@app.command
def update_readme_history(verbosity: TyroVerbosityArgType = 1) -> None:
    """
    Update project history base on git commits/tags in README.md

    Will always exist with exit code 0 because changed README is auto added to git.

    Also, callable via e.g.:
        python -m cli_base update-readme-history -v
    """
    setup_logging(verbosity=verbosity)

    logger.debug('%s called. CWD: %s', __name__, Path.cwd())
    git_history.update_readme_history(verbosity=verbosity)

    exit_code = 0  # Always exit with 0 because changed README is added to git.
    print(f'Exit with {exit_code=}')
    sys.exit(exit_code)

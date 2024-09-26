"""
    CLI for development
"""

import importlib
import logging
import sys

from bx_py_utils.path import assert_is_file
from typeguard import install_import_hook

import cli_base
from cli_base import constants
from cli_base.autodiscover import import_all_files
from cli_base.cli_tools.dev_tools import run_coverage, run_tox, run_unittest_cli
from cli_base.cli_tools.rich_utils import rich_traceback_install
from cli_base.cli_tools.version_info import print_version
from cli_base.tyro_commands import TyroCommandCli


# Check type annotations via typeguard in all tests.
# Sadly we must activate this here and can't do this in ./tests/__init__.py
install_import_hook(packages=('cli_base',))

# reload the module, after the typeguard import hook is activated:
importlib.reload(cli_base)


logger = logging.getLogger(__name__)


PACKAGE_ROOT = constants.BASE_PATH.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')  # Exists only in cloned git repo


cli = TyroCommandCli()


# Register all CLI commands, just by import all files in this package:
import_all_files(package=__package__, init_file=__file__)


@cli.register
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


def main():
    print_version(cli_base)

    rich_traceback_install()

    if len(sys.argv) >= 2:
        # Check if we can just pass a command call to origin CLI:
        command = sys.argv[1]
        command_map = {
            'test': run_unittest_cli,
            'tox': run_tox,
            'coverage': run_coverage,
        }
        if real_func := command_map.get(command):
            real_func(argv=sys.argv, exit_after_run=True)

    cli.run(
        prog='./dev-cli.py',
        description=constants.CLI_EPILOG,
    )

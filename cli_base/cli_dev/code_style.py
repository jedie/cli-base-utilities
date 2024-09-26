from cli_base.cli_dev import PACKAGE_ROOT, cli
from cli_base.cli_tools import code_style
from cli_base.tyro_commands import TyroVerbosityArgType


@cli.register
def fix_code_style(verbosity: TyroVerbosityArgType, color: bool = True):
    """
    Fix code style of all cli_base source code files via darker
    """
    code_style.fix(package_root=PACKAGE_ROOT, darker_color=color, darker_verbose=verbosity > 0)


@cli.register
def check_code_style(verbosity: TyroVerbosityArgType, color: bool = True):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=PACKAGE_ROOT, darker_color=color, darker_verbose=verbosity > 0)

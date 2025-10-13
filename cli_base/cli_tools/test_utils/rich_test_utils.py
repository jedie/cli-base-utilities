import io
import os
import re
import subprocess
import sys
from unittest.mock import patch

import rich
from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.path import assert_is_file
from bx_py_utils.test_utils.context_managers import MassContextManager
from rich import get_console
from rich.console import Console, get_windows_console_features

from cli_base.cli_tools.subprocess_utils import verbose_check_output
from cli_base.cli_tools.test_utils.assertion import assert_in


BASE_WIDTH = 120

FIX_TERM_DICT = dict(
    PYTHONUNBUFFERED='1',
    COLUMNS=str(BASE_WIDTH),
    TERM='dump',
    NO_COLOR='1',
    COLORTERM=None,
    FORCE_COLOR=None,
)


def get_fixed_env_copy(width: int = BASE_WIDTH, exclude_none=False) -> dict:
    env_dict = FIX_TERM_DICT.copy()
    env_dict['COLUMNS'] = str(width)
    if exclude_none:
        env_dict = {key: value for key, value in env_dict.items() if value is not None}
    return env_dict


def get_fixed_console(width=50) -> Console:
    """
    Get a console with a defined width and no colors. Used for testing.
    """
    console = Console(
        width=width,
        file=io.StringIO(),
        color_system=None,
        force_terminal=True,
        legacy_windows=False,
        _environ={},
    )
    return console


class NoColorTermEnviron(MassContextManager):
    """
    Context manager that set all environment variables to deactivate terminal colors and fix the terminal width
    """

    def __init__(self, width: int = BASE_WIDTH):
        self.mocks = [
            OverrideEnviron(
                **get_fixed_env_copy(width),
            ),
        ]


class NoColorEnvRich(NoColorTermEnviron):
    """
    Context manager that patch "rich" console to a no-color with a defined width.
    """

    def __init__(self, width: int = BASE_WIDTH):
        super().__init__(width)
        self.mocks += [
            patch.object(rich, '_console', Console(width=width, no_color=True)),
            patch.object(Console, '_environ', get_fixed_env_copy(width, exclude_none=True)),
        ]


# Borrowed from click:
_ansi_re = re.compile(r'\033\[[;?0-9]*[a-zA-Z]')


def strip_ansi_codes(value: str) -> str:
    return _ansi_re.sub('', value)


def invoke(
    *,
    cli_bin,
    args,
    strip_line_prefix: str = '',
    exit_on_error: bool = True,
    strip_ansi: bool = True,
) -> str:
    assert_is_file(cli_bin)

    stdout = verbose_check_output(
        cli_bin,
        *args,
        cwd=cli_bin.parent,
        exit_on_error=exit_on_error,
    )

    if strip_ansi:
        stdout = strip_ansi_codes(stdout)

    if strip_line_prefix:
        # Skip header lines:
        lines = stdout.splitlines()
        found = False
        for pos, line in enumerate(lines):
            if line.lstrip().startswith(strip_line_prefix):
                stdout = '\n'.join(lines[pos:])
                found = True
                break

        assert found is True, f'Line that starts with {strip_line_prefix=} not found in: {stdout!r}'

        stdout = '\n'.join(line.rstrip() for line in stdout.splitlines())

    return stdout


def assert_no_color_env(*, width: int) -> None:
    assert os.environ['COLUMNS'] == str(width), f'{os.environ["COLUMNS"]=} is not "{width=}"'
    assert os.environ['TERM'] == 'dump', f'{os.environ["TERM"]=} is not "dump"'
    assert os.environ['NO_COLOR'] == '1', f'{os.environ["NO_COLOR"]=} is not "1"'


def assert_subprocess_rich_diagnose_no_color(*, width: int) -> None:
    output = subprocess.check_output(
        [sys.executable, '-m', 'rich.diagnose'],
        text=True,
        env=os.environ.copy(),  # It's needed to pass the current environment!
    )
    assert_in(
        output,
        parts=(
            f'width={width}',
            'color_system = None',
            'no_color = True',
            'highlight=None,',
            'style = None',
            'truecolor = False',
            'vt = False',
        ),
    )


def assert_rich_no_color(*, width: int) -> None:
    features = get_windows_console_features()
    assert features.truecolor is False, f'{features=}'

    global_console = get_console()
    assert global_console._width == width, f'{global_console._width=} is not {width=}'
    assert global_console.no_color is True

    new_console = Console()
    assert new_console._width == width, f'{new_console._width=} is not {width=}'
    assert new_console.no_color is True

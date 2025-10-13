#
# *** All tools here are DEPRECATED! ***
#

import warnings
from unittest.mock import patch

import rich_click

from cli_base.cli_tools.test_utils.rich_test_utils import BASE_WIDTH, NoColorEnvRich, invoke


class NoColorEnvRichClick(NoColorEnvRich):
    """
    Context manager for rich-click to deactivate terminal colors and fix the terminal width
    """

    def __init__(self, width: int = BASE_WIDTH):
        super().__init__(width)
        warnings.warn(
            'This context manager is deprecated.',
            DeprecationWarning,
            stacklevel=2,
        )
        self.mocks += [
            patch.object(rich_click.rich_click, 'MAX_WIDTH', width),
            patch.object(rich_click.rich_click, 'FORCE_TERMINAL', False),
        ]


class NoColorRichClickCli(NoColorEnvRichClick):
    """
    Context manager to get the output of a rich-click CLI command.
    To re-evaluate module-level code, call the CLI via a subprocess.
    """

    def invoke(self, *args, **kwargs):
        warnings.warn(
            'This context manager is deprecated. Use invoke() instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return invoke(*args, **kwargs)


def assert_rich_click_no_color(*, width: int) -> None:
    assert rich_click.rich_click.MAX_WIDTH == width, f'{rich_click.rich_click.MAX_WIDTH=} is not "{width}"'
    assert rich_click.rich_click.FORCE_TERMINAL is False, f'{rich_click.rich_click.FORCE_TERMINAL=} is not False'

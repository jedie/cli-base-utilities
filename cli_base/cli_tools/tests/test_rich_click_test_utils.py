from unittest import TestCase

from cli_base import __version__
from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.test_utils.assertion import assert_in, assert_startswith
from cli_base.cli_tools.test_utils.rich_click_test_utils import (
    NoColorEnvRichClick,
    NoColorRichClickCli,
    assert_rich_click_no_color,
)
from cli_base.cli_tools.test_utils.rich_test_utils import (
    assert_no_color_env,
    assert_rich_no_color,
    assert_subprocess_rich_diagnose_no_color,
    invoke,
)


class MockRichTestCase(TestCase):
    def test_NoColorEnvRichClick(self):
        with NoColorEnvRichClick(width=100):
            assert_no_color_env(width=100)
            assert_subprocess_rich_diagnose_no_color(width=100)
            assert_rich_no_color(width=100)

            assert_rich_click_no_color(width=100)

    def test_NoColorRichClickCli(self):
        with NoColorRichClickCli() as cm:
            # Without "strip_line_prefix":
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=('--help',))
            assert_in(
                stdout,
                parts=(
                    '.venv/bin/cli_base_dev --help',
                    f'cli_base v{__version__}',
                    'usage: ./dev-cli.py',
                    'show this help message and exit',
                ),
            )
            assert_startswith(stdout, f'\n+ {PACKAGE_ROOT}')

            with self.assertWarns(DeprecationWarning):
                stdout = cm.invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=('--help',), strip_line_prefix='usage: ')
            assert_in(
                stdout,
                parts=(
                    'usage: ./dev-cli.py',
                    'show this help message and exit',
                ),
            )
            assert_startswith(stdout, 'usage: ./dev-cli.py [-h]')

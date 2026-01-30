from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from manageprojects.tests.base import BaseTestCase

from cli_base import constants
from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = PACKAGE_ROOT / 'README.md'
    assert_is_file(README_PATH)

    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_main_help(self):
        with NoColorEnvRich():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'cli.py', args=['--help'], strip_line_prefix='usage: ')
        assert_in(
            content=stdout,
            parts=(
                'usage: ./cli.py [-h]',
                ' version ',
                ' update-readme-history ',  # Not in dev-cli.py! Because it's used by pre-commit hook!
                'Print version and exit',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_dev_help(self):
        with NoColorEnvRich():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=['--help'], strip_line_prefix='usage: ')
        assert_in(
            content=stdout,
            parts=(
                'usage: ./dev-cli.py [-h]',
                ' lint ',
                ' coverage ',
                ' publish ',
                constants.CLI_EPILOG,
            ),
        )

        assert_cli_help_in_readme(text_block=stdout, marker='dev help')

    def test_demo_help(self):
        with NoColorEnvRich():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'demo-cli.py', args=['--help'], strip_line_prefix='usage: ')
        assert_in(
            content=stdout,
            parts=(
                'usage: ./demo-cli.py [-h]',
                ' edit-settings ',
                ' demo-endless-loop ',
                constants.CLI_EPILOG,
            ),
        )

        assert_cli_help_in_readme(text_block=stdout, marker='demo help')

from unittest import TestCase

from bx_py_utils.auto_doc import assert_readme_block

from cli_base.cli.dev import PACKAGE_ROOT
from cli_base.cli_tools.git_history import get_git_history


class ReadmeHistoryTestCase(TestCase):
    def test_readme_history(self):
        history = '\n'.join(get_git_history(add_author=False))
        assert_readme_block(
            readme_path=PACKAGE_ROOT / 'README.md',
            text_block=f'\n{history}\n',
            start_marker_line='[comment]: <> (✂✂✂ auto generated history start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated history end ✂✂✂)',
        )

from unittest import TestCase

from bx_py_utils.auto_doc import assert_readme_block

import cli_base
from cli_base.cli.dev import PACKAGE_ROOT
from cli_base.cli_tools.git_history import get_git_history


class ReadmeHistoryTestCase(TestCase):
    def test_readme_history(self):
        git_history = get_git_history(
            current_version=cli_base.__version__,
            add_author=False,
        )
        history = '\n'.join(git_history)
        assert_readme_block(
            readme_path=PACKAGE_ROOT / 'README.md',
            text_block=f'\n{history}\n',
            start_marker_line='[comment]: <> (✂✂✂ auto generated history start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated history end ✂✂✂)',
        )

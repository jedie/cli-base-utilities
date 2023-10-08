from manageprojects.tests.base import BaseTestCase

import cli_base
from cli_base.cli_tools.git_history import get_git_history


class GitHistoryTestCase(BaseTestCase):
    def test_happy_path(self):
        result = '\n'.join(get_git_history(current_version=cli_base.__version__, add_author=False))
        self.assert_in_content(
            got=result,
            parts=(
                '* [v0.4.0](https://github.com/jedie/cli-base-utilities/compare/v0.3.0...v0.4.0)',
                '  * 2023-10-08 - NEW: Generate a project history base on git commits/tags.',
            ),
        )

        result = '\n'.join(get_git_history(current_version=cli_base.__version__, add_author=True))
        self.assert_in_content(
            got=result,
            parts=('  * 2023-10-08 JensDiemer - NEW: Generate a project history base on git commits/tags.',),
        )

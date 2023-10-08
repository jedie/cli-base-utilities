from manageprojects.tests.base import BaseTestCase

from cli_base.cli_tools.git_history import get_git_history


class GitHistoryTestCase(BaseTestCase):
    def test_happy_path(self):
        result = '\n'.join(get_git_history(add_author=False))
        self.assert_in_content(
            got=result,
            parts=(
                '* [**dev**](https://github.com/jedie/cli-base-utilities/compare/',
                '* [v0.4.0](https://github.com/jedie/cli-base-utilities/compare/v0.3.0...v0.4.0)',
                '  * [2023-09-24](https://github.com/jedie/cli-base-utilities/commit/af99097) - fix tests',
            ),
        )

        result = '\n'.join(get_git_history(add_author=True))
        self.assert_in_content(
            got=result,
            parts=('* [2023-09-24 JensDiemer](https://github.com/jedie/cli-base-utilities/commit/af99097)',),
        )

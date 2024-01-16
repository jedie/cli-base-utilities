import inspect
import os
from unittest.mock import patch

import typeguard
from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.tests.base import BaseTestCase

import cli_base
from cli_base.cli_tools.git import NoGitRepoError
from cli_base.cli_tools.git_history import get_git_history, update_readme_history
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.environment_fixtures import MockCurrentWorkDir
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRichClick


class GitHistoryTestCase(BaseTestCase):
    def test_get_git_history_happy_path(self):
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

    # FIXME: remove "suppress_type_checks" after:
    # https://github.com/boxine/bx_py_utils/pull/164/files#diff-421e2a471c4deb91b133844c2caffb339a68dbebf82a65e798bbdf68b3b4013c
    @typeguard.suppress_type_checks
    def test_update_readme_history(self):
        with NoColorEnvRichClick(), MockCurrentWorkDir(prefix='test_update_readme_history') as mocked_cwd:
            temp_path = mocked_cwd.temp_path

            with self.assertRaises(FileNotFoundError) as cm:
                update_readme_history()
            self.assertIn('/pyproject.toml', str(cm.exception))

            pyproject_toml_path = temp_path / 'pyproject.toml'
            pyproject_toml_path.touch()

            with self.assertRaises(FileNotFoundError) as cm:
                update_readme_history()
            self.assertIn('/README.md', str(cm.exception))

            readme_path = temp_path / 'README.md'
            readme_path.touch()

            with self.assertRaises(LookupError) as cm:
                update_readme_history()
            self.assertIn('No "tool.cli_base.version_module_name" in ', str(cm.exception))

            pyproject_toml_path.write_text('[tool.cli_base]\nversion_module_name = "not_existing_module_name"\n')

            with self.assertRaises(ModuleNotFoundError) as cm:
                update_readme_history()
            self.assertIn('not_existing_module_name', str(cm.exception))

            pyproject_toml_path.write_text('[tool.cli_base]\nversion_module_name = "cli_base"\n')

            with self.assertRaises(NoGitRepoError) as cm:
                update_readme_history()
            self.assertIn('is not a git repository', str(cm.exception))

            with patch(
                'cli_base.cli_tools.git_history.get_git_history',
                return_value=['mocked', 'get_git_history()'],
            ):
                with self.assertRaises(AssertionError) as cm:
                    update_readme_history()
                self.assertIn(
                    "Start marker '[comment]: <> (✂✂✂ auto generated history start ✂✂✂)' not found ", str(cm.exception)
                )

                readme_path.write_text(inspect.cleandoc("""
                        before content
                        [comment]: <> (✂✂✂ auto generated history start ✂✂✂)
                        [comment]: <> (✂✂✂ auto generated history end ✂✂✂)
                        after content
                        """))

                # The mtime will be checked. This test may be to fast to have a mtime difference.
                # So set a very old mtime:
                os.utime(readme_path, (123, 456))

                with RedirectOut() as buffer:
                    updated = update_readme_history()
                self.assertIs(updated, True)
                self.assertEqual(buffer.stderr, '')
                self.assertIn('/README.md updated', buffer.stdout)

                assert_in(
                    content=readme_path.read_text(),
                    parts=(
                        'before content',
                        'mocked',
                        'get_git_history()',
                        'after content',
                    ),
                )

                # Call again, without changes:
                with RedirectOut() as buffer:
                    updated = update_readme_history()
                self.assertIs(updated, False)
                self.assertEqual(buffer.stderr, '')
                self.assertIn('/README.md is up-to-date', buffer.stdout)

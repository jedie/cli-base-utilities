import inspect
import logging
import os
from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.tests.base import BaseTestCase

import cli_base
from cli_base.cli_tools.git import Git, GitError, NoGitRepoError
from cli_base.cli_tools.git_history import get_git_history, update_readme_history
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.base_testcases import (
    LoggingMustBeCapturedTestCaseMixin,
    OutputMustCapturedTestCaseMixin,
)
from cli_base.cli_tools.test_utils.environment_fixtures import MockCurrentWorkDir
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich


class GitHistoryTestCase(OutputMustCapturedTestCaseMixin, LoggingMustBeCapturedTestCaseMixin, BaseTestCase):
    def test_get_git_history_happy_path(self):
        with self.assertLogs(level=logging.DEBUG), RedirectOut() as out_buffer:
            git = Git()
            git_history = get_git_history(git=git, current_version=cli_base.__version__, add_author=False)
            result = '\n'.join(git_history)
        assert_in(
            content=result,
            parts=(
                '* [v0.4.0](https://github.com/jedie/cli-base-utilities/compare/v0.3.0...v0.4.0)',
                '  * 2023-10-08 - NEW: Generate a project history base on git commits/tags.',
            ),
        )
        self.assertEqual(out_buffer.stderr, '')

        with self.assertLogs(level=logging.DEBUG), RedirectOut() as out_buffer:
            git_history = get_git_history(git=git, current_version=cli_base.__version__, add_author=True)
            result = '\n'.join(git_history)
        assert_in(
            content=result,
            parts=('  * 2023-10-08 JensDiemer - NEW: Generate a project history base on git commits/tags.',),
        )
        self.assertEqual(out_buffer.stderr, '')

    def test_update_readme_history(self):
        with (
            NoColorEnvRich(),
            MockCurrentWorkDir(prefix='test_update_readme_history') as mocked_cwd,
            self.assertLogs(level=logging.DEBUG),
            RedirectOut() as out_buffer,
        ):
            temp_path = mocked_cwd.temp_path

            with self.assertRaises(NoGitRepoError) as cm:
                update_readme_history()
            self.assertEqual(str(cm.exception), f'"{temp_path}" is not a git repository')

            # Initialize a git repo:
            git = Git(cwd=temp_path, detect_root=False)
            git.init()

            # pyproject.toml is missing:
            with self.assertRaises(FileNotFoundError) as cm:
                update_readme_history()
            self.assertIn('/pyproject.toml', str(cm.exception))

            pyproject_toml_path = temp_path / 'pyproject.toml'
            pyproject_toml_path.touch()

            # README.md is missing:
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

            with self.assertRaises(GitError) as cm:
                update_readme_history()
            self.assertEqual(str(cm.exception), 'Git main branch not found in: []')

            git.add('.', verbose=False)
            git.commit(comment='Update pyproject.toml', verbose=False)

            with self.assertRaises(AssertionError) as cm:
                update_readme_history()
            self.assertIn(
                "Start marker '[comment]: <> (✂✂✂ auto generated history start ✂✂✂)' not found ", str(cm.exception)
            )

            readme_path.write_text(
                inspect.cleandoc("""
                    before content
                    [comment]: <> (✂✂✂ auto generated history start ✂✂✂)
                    [comment]: <> (✂✂✂ auto generated history end ✂✂✂)
                    after content
                """)
            )

            # The mtime will be checked. This test may be to fast to have a mtime difference.
            # So set a very old mtime:
            os.utime(readme_path, (123, 456))

            with patch('cli_base.cli_tools.git_history.get_git_history', return_value=['mocked', 'get_git_history()']):
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
                self.assertEqual(buffer.stderr, '')
                self.assertIn('/README.md is up-to-date', buffer.stdout)
                self.assertIs(updated, False)
        self.assertEqual(out_buffer.stderr, '')

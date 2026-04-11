from pathlib import Path

from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.utilities.temp_path import TemporaryDirectory

import cli_base
from cli_base import __version__
from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.git import Git
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.base_testcases import BaseTestCase
from cli_base.cli_tools.test_utils.logs import AssertLogs
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich
from cli_base.cli_tools.version_info import print_version


class VersionInfoTestCase(BaseTestCase):
    maxDiff = None

    def test_temp_content_file(self):
        git = Git(cwd=PACKAGE_ROOT)
        git_hash = git.get_current_hash(verbose=False)

        with NoColorEnvRich(), RedirectOut() as buffer:
            print_version(module=cli_base)

        self.assertEqual(buffer.stderr, '')
        self.assertEqual(buffer.stdout, f'cli-base v{__version__} {git_hash} ({PACKAGE_ROOT})\n')

        with NoColorEnvRich(), RedirectOut() as buffer:
            print_version(module=cli_base, project_name='cli-base-utilities')

        self.assertEqual(buffer.stderr, '')
        self.assertEqual(buffer.stdout, f'cli-base-utilities v{__version__} {git_hash} ({PACKAGE_ROOT})\n')

    def test_no_git(self):
        with NoColorEnvRich(), RedirectOut() as buffer:
            print_version(module=cli_base, project_root=Path('foo', 'bar'))

        self.assertEqual(buffer.stderr, '')
        self.assertEqual(buffer.stdout, f'cli-base v{__version__} (No git found for: foo/bar)\n')

        with TemporaryDirectory(prefix='test_no_git') as temp_path:
            non_git_path = temp_path / '.git'
            non_git_path.mkdir()

            with NoColorEnvRich(), AssertLogs(self, loggers=('cli_base',)) as logs, RedirectOut() as buffer:
                print_version(module=cli_base, project_root=temp_path)

            assert_in(
                content=buffer.stdout,
                parts=(
                    f'cli-base v{__version__} ',
                    'print version error:',
                ),
            )

            logs.assert_in('Error print version', 'Traceback')

import os
import tempfile
from pathlib import Path
from unittest import TestCase

from cli_base.cli_tools.path_utils import backup, expand_user, which
from cli_base.cli_tools.test_utils.environment_fixtures import AsSudoCallOverrideEnviron
from cli_base.cli_tools.test_utils.logs import AssertLogs
from cli_base.constants import PY_BIN_PATH


class PathUtilsTestCase(TestCase):
    def test_expand_user(self):
        real_home_path = Path.home()
        real_example = Path('~/example/').expanduser()

        self.assertEqual(expand_user(Path('~')), real_home_path)
        self.assertEqual(expand_user(Path('~/example/')), real_example)

        with AsSudoCallOverrideEnviron():
            self.assertEqual(Path('~').expanduser(), Path('/root'))
            self.assertEqual(expand_user(Path('~')), real_home_path)

            self.assertEqual(Path('~/example/').expanduser(), Path('/root/example'))
            self.assertEqual(expand_user(Path('~/example/')), real_example)

        # What happen if SUDO_USER is the same as getpass.getuser() ?
        with AsSudoCallOverrideEnviron(SUDO_USER='root', LOGNAME='root'), AssertLogs(
            self, loggers=('cli_base',)
        ) as logs:
            self.assertEqual(Path('~').expanduser(), Path('/root'))
            self.assertEqual(expand_user(Path('~')), Path('/root'))
        logs.assert_in('Do not run this as root user!', "SUDO_USER:'root' <-> root")

    def test_backup(self):
        with tempfile.TemporaryDirectory(prefix='test_') as temp_dir:
            temp_path = Path(temp_dir)

            test_path = temp_path / 'foobar.ext'
            test_path.write_text('one')

            bak1_path = backup(test_path)
            self.assertEqual(bak1_path, temp_path / 'foobar.ext.bak')
            self.assertEqual(bak1_path.read_text(), 'one')

            test_path.write_text('two')

            bak2_path = backup(test_path)
            self.assertEqual(bak2_path, temp_path / 'foobar.ext.bak2')
            self.assertEqual(bak2_path.read_text(), 'two')

            test_path.write_text('three')

            bak3_path = backup(test_path)
            self.assertEqual(bak3_path, temp_path / 'foobar.ext.bak3')
            self.assertEqual(bak3_path.read_text(), 'three')

            with self.assertRaises(RuntimeError) as cm:
                backup(test_path, max_try=3)
            self.assertEqual(cm.exception.args, ('No backup made: Maximum attempts to find a file name failed.',))

    def test_which(self):
        with tempfile.TemporaryDirectory(prefix='test_') as temp_dir:
            temp_path = Path(temp_dir)

            UNIQUE_FILE_NAME = 'this-is-the-test-tool'
            self.assertIs(which(UNIQUE_FILE_NAME), None)

            fake_tool_path = temp_path / UNIQUE_FILE_NAME
            fake_tool_path.touch(mode=0o777)
            self.assertIs(which(UNIQUE_FILE_NAME), None)
            self.assertEqual(
                which(tool_name=UNIQUE_FILE_NAME, path=temp_path),
                fake_tool_path,
            )

            # Must be executable as default:
            fake_tool_path.chmod(0o666)
            self.assertIs(
                which(tool_name=UNIQUE_FILE_NAME, path=temp_path),
                None,
            )

            # Or just a file:
            self.assertEqual(
                which(tool_name=UNIQUE_FILE_NAME, mode=os.F_OK, path=temp_path),
                fake_tool_path,
            )

        python_path = which('python')
        self.assertIsInstance(python_path, Path)
        self.assertEqual(python_path.name, 'python')
        self.assertEqual(python_path.parent, PY_BIN_PATH)  # our venv interpreter?

        # "ls" command should be available on all systems, isn't it?
        tool_path = which('ls')
        self.assertIsInstance(tool_path, Path)
        self.assertEqual(tool_path.name, 'ls')

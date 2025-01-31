from pathlib import PosixPath
from unittest import TestCase
from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.test_utils.subprocess import Call, SubprocessCallMock

from cli_base.cli_tools import path_utils
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.shutil_mocks import ShutilWhichMock
from cli_base.toml_settings.sensible_editor import open_editor_for


class SensibleEditorTestCase(TestCase):
    def test_open_editor_for(self):
        which_mock = ShutilWhichMock(
            command_map={
                'sensible-editor': None,
                'mcedit': None,
                'nano': '/foo/bar/bin/nano',
            }
        )
        with SubprocessCallMock() as subprocess_mock, patch.object(path_utils, 'shutil', which_mock):
            open_editor_for(file_path='/file/path/foo.txt')

        self.assertEqual(
            subprocess_mock.calls,
            [
                Call(
                    popenargs=[PosixPath('/foo/bar/bin/nano'), '/file/path/foo.txt'],
                    args=(),
                    kwargs={},
                )
            ],
        )

    def test_open_editor_for_no_editor_found(self):
        which_mock = ShutilWhichMock(
            command_map={
                'sensible-editor': None,
                'mcedit': None,
                'nano': None,
                'edit': None,
                'open': None,
            }
        )
        with (
            SubprocessCallMock() as subprocess_mock,
            patch.object(path_utils, 'shutil', which_mock),
            RedirectOut() as buffer,
        ):
            with self.assertRaises(SystemExit):
                open_editor_for(file_path='/file/path/foo.txt')

        self.assertEqual(buffer.stderr, '')
        assert_in(
            content=buffer.stdout,
            parts=(
                'Error: No way found to open "/file/path/foo.txt" !',
                '(Tried: sensible-editor, mcedit, nano, edit, open)',
            ),
        )
        self.assertEqual(subprocess_mock.calls, [])

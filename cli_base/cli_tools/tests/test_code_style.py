from unittest import TestCase

from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.code_style import assert_code_style
from cli_base.constants import PY_BIN_PATH


class CodeStyleTestCase(TestCase):
    def test_code_style_calls(self):
        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            assert_code_style(package_root=PACKAGE_ROOT)
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [['.../ruff', 'check', '--fix']]
        )

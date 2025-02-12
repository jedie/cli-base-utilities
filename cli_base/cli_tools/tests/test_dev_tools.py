import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.dev_tools import EraseCoverageData, run_coverage, run_nox, run_unittest_cli
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorTermEnviron, invoke
from cli_base.constants import PY_BIN_PATH


PYTHON_NAME = Path(sys.executable).name


class DevToolsTestCase(TestCase):
    def test_erase_coverage_data(self):
        erase_coverage_data = EraseCoverageData()
        erase_coverage_data.erased = False

        with patch('cli_base.cli_tools.subprocess_utils.verbose_check_call') as func_mock:
            erase_coverage_data(
                argv=('./dev-cli.py', 'coverage'),  # no "--verbose"
            )
        func_mock.assert_called_once()
        self.assertIs(erase_coverage_data.erased, True)

        # Skip on second call:
        with patch('cli_base.cli_tools.subprocess_utils.verbose_check_call') as func_mock:
            erase_coverage_data()
        func_mock.assert_not_called()
        self.assertIs(erase_coverage_data.erased, True)

    def test_run_unittest(self):
        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            run_unittest_cli(argv=('./dev-cli.py', 'unittest'), exit_after_run=False)
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [
                [f'.../{PYTHON_NAME}', '-m', 'unittest', '--locals', '--buffer'],
            ],
        )

    def test_run_unittest_via_cli(self):
        with NoColorTermEnviron():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=('test', '--help'))
        assert_in(
            stdout,
            parts=(
                'unittest --help',
                'usage: python',
                ' -m unittest [-h]',
            ),
        )

    def test_run_nox(self):
        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            run_nox(argv=('./dev-cli.py', 'nox'), exit_after_run=False)
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [
                ['.../nox'],
                ['.../coverage', 'combine', '--append'],
                ['.../coverage', 'report'],
                ['.../coverage', 'xml'],
                ['.../coverage', 'json'],
            ],
        )

    def test_run_nox_via_cli(self):
        with NoColorTermEnviron():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=('nox', '--help'))
        assert_in(
            stdout,
            parts=(
                'nox --help',
                'usage: nox [-h]',
            ),
        )

    def test_run_coverage(self):
        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            run_coverage(argv=('./dev-cli.py', 'coverage'), exit_after_run=False)
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [
                ['.../coverage', 'run'],
                ['.../coverage', 'combine', '--append'],
                ['.../coverage', 'report'],
                ['.../coverage', 'xml'],
                ['.../coverage', 'json'],
                ['.../coverage', 'erase'],
            ],
        )

        # help will not combine report and erase data:
        with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
            try:
                run_coverage(argv=('./dev-cli.py', 'coverage', '--help'))
            except SystemExit as err:
                self.assertEqual(err.code, 0)
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [['.../coverage', '--help']],
        )

    def test_run_coverage_via_cli(self):
        with NoColorTermEnviron():
            stdout = invoke(cli_bin=PACKAGE_ROOT / 'dev-cli.py', args=('coverage', '--help'))
        assert_in(
            stdout,
            parts=(
                '.venv/bin/cli_base_dev coverage --help',
                'Coverage.py',
                'usage: coverage <command> [options] [args]',
            ),
        )

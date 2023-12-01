from unittest import TestCase
from unittest.mock import patch

from cli_base.cli_tools.dev_tools import EraseCoverageData


class DevToolsTestCase(TestCase):
    def test_erase_coverage_data(self):
        erase_coverage_data = EraseCoverageData()
        erase_coverage_data.erased = False

        with patch('cli_base.cli_tools.dev_tools.verbose_check_call') as func_mock:
            erase_coverage_data()
        func_mock.assert_called_once_with('coverage', 'erase', verbose=True, exit_on_error=True, cwd=None)
        self.assertIs(erase_coverage_data.erased, True)

        # Skip on second call:
        with patch('cli_base.cli_tools.dev_tools.verbose_check_call') as func_mock:
            erase_coverage_data()
        func_mock.assert_not_called()
        self.assertIs(erase_coverage_data.erased, True)

import unittest
from pathlib import Path

from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.test_utils.assertion import assert_startswith


class ToolsExecutorTestCase(unittest.TestCase):

    def test_happy_path(self):
        executor = ToolsExecutor()
        self.assertEqual(executor.cwd, Path.cwd())
        self.assertIn('PYTHONUNBUFFERED', executor.extra_env)

        self.assertFalse(executor.is_executable('foo-bar'))
        self.assertTrue(executor.is_executable('python'))

        return_code = executor.verbose_check_call('python', '--version')
        self.assertEqual(return_code, 0)

        output = executor.verbose_check_output('python', '--version')
        assert_startswith(output, 'Python 3.')

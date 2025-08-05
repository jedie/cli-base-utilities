import unittest
from pathlib import Path

from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.test_utils.assertion import assert_startswith
from cli_base.cli_tools.test_utils.subprocess_mocks import MockToolsExecutor
from cli_base.cli_tools.tests import tools_executer_test_helper


class ToolsExecutorTestCase(unittest.TestCase):
    maxDiff = None

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

    def test_tool_executor_mock(self):
        with MockToolsExecutor(
            target=tools_executer_test_helper,
            return_codes={'foo': 0},
            outputs={
                'Foo': 'Foo 1.2.3\n',
                'Bar': 'Bar was called',
            },
        ) as mock:
            tools_executer_test_helper.call_tools_executor()

        self.assertEqual(
            mock.calls,
            [
                {'file_name': 'foo'},
                {'file_name': 'Foo', 'popenargs': ('--version',)},
                {'file_name': 'Bar', 'kwargs': {'cwd': '/some/where/else'}},
            ],
        )
        self.assertIs(mock.cwd, None)

        with MockToolsExecutor(
            target=tools_executer_test_helper,
            return_codes={'foo': 0},
            outputs={
                'Foo': 'Foo 1.2.3\n',
                'Bar': 'Bar was called',
            },
        ) as mock:
            tools_executer_test_helper.call_tools_executor(cwd='/some/where/')
        self.assertIs(mock.cwd, '/some/where/')

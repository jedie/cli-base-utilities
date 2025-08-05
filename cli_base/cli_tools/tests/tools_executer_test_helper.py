from cli_base.cli_tools.subprocess_utils import ToolsExecutor


def call_tools_executor(cwd=None):
    executor = ToolsExecutor(cwd=cwd)

    return_code = executor.verbose_check_call('foo')
    assert return_code == 0, f'{return_code=}'

    output = executor.verbose_check_output('Foo', '--version')
    assert output == 'Foo 1.2.3\n', f'{output=}'
    output = executor.verbose_check_output('Bar', cwd='/some/where/else')
    assert output == 'Bar was called', f'{output=}'

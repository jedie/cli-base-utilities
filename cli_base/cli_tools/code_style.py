from __future__ import annotations

import sys
from pathlib import Path
from subprocess import CalledProcessError

from cli_base.cli_tools.subprocess_utils import ToolsExecutor


def assert_code_style(
    package_root: Path,
    verbose: bool = True,
    sys_exit: bool = False,
) -> int:
    """
    Helper for code style check and autofix in unittests.
    usage e.g.:

        def test_code_style(self):
            return_code = assert_code_style(package_root=PACKAGE_ROOT)
            self.assertEqual(return_code, 0, 'Code style error, see output above!')

    But can also be used in CLI commands, e.g.:

        @app.command
        def lint(verbosity: TyroVerbosityArgType = 1):
            assert_code_style(package_root=PACKAGE_ROOT, verbose=bool(verbosity), sys_exit=True)
    """
    tools_executor = ToolsExecutor(cwd=package_root)
    try:
        tools_executor.verbose_check_call(
            'ruff',
            'check',
            '--fix',
            verbose=verbose,
            exit_on_error=False,
        )
    except SystemExit as err:
        return_code = err.code
    except CalledProcessError as err:
        return_code = err.returncode
    else:
        return_code = 0

    if sys_exit:
        sys.exit(return_code)
    else:
        return return_code

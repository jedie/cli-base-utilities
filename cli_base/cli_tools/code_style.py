from __future__ import annotations

import dataclasses
import sys
from pathlib import Path
from subprocess import CalledProcessError

from cli_base.cli_tools.subprocess_utils import ToolsExecutor


@dataclasses.dataclass
class DarkerResult:
    return_code: int
    output: str | None = None

    @property
    def status(self) -> str:
        return 'OK' if self.return_code == 0 else 'ERROR'


def _call_darker(
    *args,
    package_root: Path,
    darker_color: bool = True,
    darker_quiet: bool = False,
    darker_verbose: bool = False,
    verbose_call: bool = True,
    capture_output: bool = False,
) -> DarkerResult:
    final_args = ['darker']

    if darker_verbose:
        final_args.append('--verbose')
    elif darker_quiet:
        final_args.append('--quiet')

    if darker_color:
        final_args.append('--color')
    else:
        final_args.append('--no-color')

    final_args += list(args)

    tools_executor = ToolsExecutor(cwd=package_root)

    if capture_output:
        try:
            output = tools_executor.verbose_check_output(
                *final_args,
                verbose=verbose_call,
                exit_on_error=False,
                print_output_on_error=False,
            )
        except CalledProcessError as err:
            return DarkerResult(return_code=err.returncode, output=err.output)
        return DarkerResult(return_code=0, output=output)
    else:
        try:
            tools_executor.verbose_check_call(
                *final_args,
                verbose=verbose_call,
                exit_on_error=False,
            )
        except SystemExit as err:
            return DarkerResult(return_code=err.code)
        except CalledProcessError as err:
            return DarkerResult(return_code=err.returncode)
        return DarkerResult(return_code=0)


def fix(
    package_root: Path,
    darker_color: bool = True,
    darker_quiet: bool = False,
    darker_verbose: bool = False,
    exit: bool = True,
    verbose_call: bool = True,
    capture_output: bool = False,
) -> DarkerResult | None:
    """
    Fix code style via darker
    """
    result: DarkerResult = _call_darker(
        darker_color=darker_color,
        darker_quiet=darker_quiet,
        darker_verbose=darker_verbose,
        package_root=package_root,
        verbose_call=verbose_call,
        capture_output=capture_output,
    )

    if darker_verbose or verbose_call:
        print(f'Fix code style: {result.status}')

    if exit:
        sys.exit(result.return_code)

    return result


def check(
    package_root: Path,
    darker_color: bool = True,
    darker_quiet: bool = False,
    darker_verbose: bool = False,
    flake_verbose: bool = False,
    exit: bool = True,
    verbose_call: bool = True,
    capture_output: bool = False,
) -> DarkerResult | None:
    """
    Check code style by calling darker + flake8
    """
    result: DarkerResult = _call_darker(
        '--check',
        darker_color=darker_color,
        darker_quiet=darker_quiet,
        darker_verbose=darker_verbose,
        package_root=package_root,
        verbose_call=verbose_call,
        capture_output=capture_output,
    )

    if flake_verbose:
        args = ['--verbose']
    else:
        args = []

    # flake8 should always be green:

    tools_executor = ToolsExecutor(cwd=package_root)
    try:
        tools_executor.verbose_check_call(
            'flake8',
            *args,
            verbose=verbose_call,
            exit_on_error=exit,
        )
    except SystemExit as err:
        if return_code := err.code:
            result.return_code = return_code
    except CalledProcessError as err:
        if return_code := err.returncode:
            result.return_code = return_code

    if darker_verbose or verbose_call:
        print(f'Code style: {result.status}')

    if exit:
        sys.exit(result.return_code)

    return result


def assert_code_style(package_root: Path) -> int:
    """
    Helper for code style check and autofix in unittests.
    usage e.g.:

        def test_code_style(self):
            return_code = assert_code_style(package_root=PACKAGE_ROOT)
            self.assertEqual(return_code, 0, 'Code style error, see output above!')
    """
    result: DarkerResult = check(
        package_root=package_root,
        darker_color=False,
        darker_quiet=True,
        darker_verbose=False,
        exit=False,
        verbose_call=False,
        capture_output=True,  # capture output -> don't print anything
    )
    if result.return_code == 0:
        # Code style is OK -> test passed
        return 0

    # Try to "auto" fix code style:

    fix(
        package_root=package_root,
        darker_color=False,
        darker_quiet=False,
        darker_verbose=False,
        exit=False,
        verbose_call=True,
        capture_output=False,  # all output to stdout
    )

    # Check again and display the output:

    result: DarkerResult = check(
        package_root=package_root,
        darker_color=True,
        darker_quiet=False,
        darker_verbose=False,
        exit=False,
        verbose_call=True,
        capture_output=False,  # all output to stdout
    )

    return result.return_code

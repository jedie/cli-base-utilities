import contextlib
import os
import sys
import warnings
from pathlib import Path
from subprocess import CalledProcessError

from cli_base.cli_tools.subprocess_utils import ToolsExecutor, verbose_check_call


def is_verbose(*, argv: list) -> bool:
    if '-v' in argv or '--verbose' in argv:
        return True
    return False


class EraseCoverageData:
    """
    Erase previously collected coverage data by call: `python3 -m coverage erase`
    """

    erased = False

    def __call__(self, *, argv=None, cwd=None, verbose=None, exit_on_error=True):
        if argv is None:
            argv = sys.argv

        if verbose is None:
            verbose = is_verbose(argv=argv)

        if not self.erased:
            tools_executor = ToolsExecutor(cwd=cwd)
            tools_executor.verbose_check_call('coverage', 'erase', verbose=verbose, exit_on_error=exit_on_error)
        self.erased = True  # Call only once at runtime!


erase_coverage_data = EraseCoverageData()


def coverage_combine_report(*, argv=None, verbose=None, exit_on_error=True, cwd: Path | None = None):
    if argv is None:
        argv = sys.argv

    if verbose is None:
        verbose = is_verbose(argv=argv)

    tools_executor = ToolsExecutor(cwd=cwd)
    tools_executor.verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=exit_on_error)
    tools_executor.verbose_check_call('coverage', 'report', verbose=verbose, exit_on_error=exit_on_error)
    tools_executor.verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=exit_on_error)
    tools_executor.verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=exit_on_error)
    erase_coverage_data(verbose=verbose, exit_on_error=exit_on_error, cwd=cwd)


def run_unittest_cli(*, argv=None, extra_env=None, verbose=None, exit_after_run=True):
    """
    Call the origin unittest CLI and pass all args to it.
    """
    if argv is None:
        argv = sys.argv

    if verbose is None:
        verbose = is_verbose(argv=argv)

    if extra_env is None:
        extra_env = dict()

    extra_env.update(
        dict(
            PYTHONUNBUFFERED='1',
            PYTHONWARNINGS='always',
        )
    )

    args = argv[2:]
    if not args:
        if verbose:
            args = ('--verbose', '--locals', '--buffer')
        else:
            args = ('--locals', '--buffer')

    return_code = 0

    try:
        verbose_check_call(
            sys.executable,
            '-m',
            'unittest',
            *args,
            timeout=15 * 60,
            extra_env=extra_env,
            exit_on_error=False,
        )
    except SystemExit as err:
        return_code = err.code
    except CalledProcessError as err:
        return_code = err.returncode
    finally:
        inside_tox_run = 'TOX_ENV_NAME' in os.environ  # Called by tox run?
        if not inside_tox_run:  # Don't erase coverage data if unittests runs via tox
            with contextlib.suppress(SystemExit):
                erase_coverage_data(verbose=verbose)

    if exit_after_run:
        if verbose:
            print(f'Exit unittest with code {return_code!r}')
        sys.exit(return_code)


def run_tox(*, argv=None, verbose=None, exit_after_run=True):
    """
    Call tox and pass all command arguments to it
    """
    warnings.warn(
        'run_tox() is deprecated. Please migrate to run_nox() instead.',
        DeprecationWarning,
        stacklevel=2,
    )

    if argv is None:
        argv = sys.argv

    if verbose is None:
        verbose = is_verbose(argv=argv)

    return_code = 0

    try:
        verbose_check_call(sys.executable, '-m', 'tox', *argv[2:])
        with contextlib.suppress(SystemExit):
            # Ignore exit code from "coverage", because tox exit code is more important here.
            coverage_combine_report(verbose=verbose)
    except SystemExit as err:
        return_code = err.code
    except CalledProcessError as err:
        return_code = err.returncode
    finally:
        with contextlib.suppress(SystemExit):
            erase_coverage_data(verbose=verbose)

    if exit_after_run:
        if verbose:
            print(f'Exit tox with code {return_code!r}')
        sys.exit(return_code)


def run_nox(*, argv=None, verbose=None, exit_after_run=True, cwd: Path | None = None):
    """
    Call nox and pass all command arguments to it
    """
    if argv is None:
        argv = sys.argv

    if verbose is None:
        verbose = is_verbose(argv=argv)

    tools_executor = ToolsExecutor(cwd=cwd)
    return_code = 0
    try:
        tools_executor.verbose_check_call('nox', *argv[2:])
        with contextlib.suppress(SystemExit):
            # Ignore exit code from "coverage", because nox exit code is more important here.
            coverage_combine_report(verbose=verbose)
    except SystemExit as err:
        return_code = err.code
    except CalledProcessError as err:
        return_code = err.returncode
    finally:
        with contextlib.suppress(SystemExit):
            erase_coverage_data(verbose=verbose)

    if exit_after_run:
        if verbose:
            print(f'Exit nox with code {return_code!r}')
        sys.exit(return_code)


def run_coverage(*, argv=None, verbose=None, exit_on_error=True, exit_after_run=True, cwd: Path | None = None):
    """
    Call coverage and pass all command arguments to it
    """
    if argv is None:
        argv = sys.argv

    if verbose is None:
        verbose = is_verbose(argv=argv)

    if len(argv) < 3:
        # Autostart coverage run if no args passed
        argv += ('run',)

    run_call = argv[2] == 'run'  # Will there by coverage data created?

    tools_executor = ToolsExecutor(cwd=cwd)
    return_code = 0
    try:
        tools_executor.verbose_check_call('coverage', *argv[2:], verbose=verbose, exit_on_error=exit_on_error)
        if run_call:
            coverage_combine_report(verbose=verbose)
    except SystemExit as err:
        return_code = err.code
    except CalledProcessError as err:
        return_code = err.returncode
    finally:
        if run_call:
            erase_coverage_data(verbose=verbose)

    if exit_after_run:
        if verbose:
            print(f'Exit coverage with code {return_code!r}')
        sys.exit(return_code)

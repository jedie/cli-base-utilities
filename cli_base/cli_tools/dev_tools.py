import os
import sys
from pathlib import Path

from cli_base.cli_tools.subprocess_utils import verbose_check_call


def is_verbose(*, argv):
    if '-v' in argv or '--verbose' in argv:
        return True
    return False


class EraseCoverageData:
    """
    Erase previously collected coverage data by call: `python3 -m coverage erase`
    """

    erased = False

    def __call__(self, *, cwd=Path().cwd(), verbose=True):
        if not self.erased:
            verbose_check_call('coverage', 'erase', verbose=verbose, exit_on_error=True, cwd=cwd)
        self.erased = True  # Call only once at runtime!


erase_coverage_data = EraseCoverageData()


def coverage_combine_report(*, cwd=Path().cwd(), verbose=True):
    verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'report', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True, cwd=cwd)
    erase_coverage_data(verbose=True)


def run_unittest_cli(extra_env=None, verbose=None, exit_after_run=True):
    """
    Call the origin unittest CLI and pass all args to it.
    """
    if verbose is None:
        verbose = is_verbose(argv=sys.argv)

    if extra_env is None:
        extra_env = dict()

    extra_env.update(
        dict(
            PYTHONUNBUFFERED='1',
            PYTHONWARNINGS='always',
        )
    )

    args = sys.argv[2:]
    if not args:
        if verbose:
            args = ('--verbose', '--locals', '--buffer')
        else:
            args = ('--locals', '--buffer')

    try:
        verbose_check_call(
            sys.executable,
            '-m',
            'unittest',
            *args,
            timeout=15 * 60,
            extra_env=extra_env,
        )
    finally:
        inside_tox_run = 'TOX_ENV_NAME' in os.environ  # Called by tox run?
        if not inside_tox_run:
            erase_coverage_data(verbose=verbose)

    if exit_after_run:
        sys.exit(0)


def run_tox():
    """
    Call tox and pass all command arguments to it
    """
    verbose = is_verbose(argv=sys.argv)
    try:
        verbose_check_call(sys.executable, '-m', 'tox', *sys.argv[2:])
    finally:
        coverage_combine_report(verbose=verbose)
        erase_coverage_data(verbose=verbose)

    sys.exit(0)

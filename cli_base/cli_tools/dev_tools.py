import sys
from pathlib import Path

from manageprojects.utilities.subprocess_utils import verbose_check_call
from rich import print


def clean_coverage_files():
    """
    Old / obsolete coverage files may corrupt the test run,
    so better try to remove them
    """
    for file_path in Path().cwd().glob('.coverage*'):
        try:
            file_path.unlink()
        except OSError as err:
            print(f'(Error remove {file_path}: {err})')
        else:
            print(f'(remove {file_path}, ok)')


def _run_unittest_cli(extra_env=None, verbose=True, exit_after_run=True):
    """
    Call the origin unittest CLI and pass all args to it.
    """
    clean_coverage_files()

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

    verbose_check_call(
        sys.executable,
        '-m',
        'unittest',
        *args,
        timeout=15 * 60,
        extra_env=extra_env,
    )
    if exit_after_run:
        sys.exit(0)


def _run_tox():
    """
    Call tox and pass all command arguments to it
    """
    clean_coverage_files()
    verbose_check_call(sys.executable, '-m', 'tox', *sys.argv[2:])
    sys.exit(0)

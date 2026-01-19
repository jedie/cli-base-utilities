import getpass
import logging
import os
import shutil
from pathlib import Path

from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.path import assert_is_file

from cli_base.constants import PY_BIN_PATH


logger = logging.getLogger(__name__)


def is_path_name(name: str) -> None:
    """
    >>> is_path_name('a_example_filename')
    >>> is_path_name('A Directory name')

    >>> is_path_name('/not/valid/')
    Traceback (most recent call last):
        ...
    AssertionError: Path name '/not/valid/' is not valid! (Not the same as: cleaned='valid')

    >>> is_path_name('invalid.exe')
    Traceback (most recent call last):
        ...
    AssertionError: Path name 'invalid.exe' is not valid! (Not the same as: cleaned='invalid')
    """
    cleaned = Path(name).stem
    if name != cleaned:
        raise AssertionError(f'Path name {name!r} is not valid! (Not the same as: {cleaned=!r})')


def expand_user(path: Path) -> Path:
    """
    Returns a new path with expanded ~ and ~user constructs:
    Unlike the normal Python function, when called with sudo, the normal user path is used.
    So "~" is not expanded as "/root" -> it's expanded with the user home that sudo starts with!
    """
    logger.debug(f'expand user path: {path}')
    if sudo_user := os.environ.get('SUDO_USER'):
        if sudo_user == 'root':
            logger.warning('Do not run this as root user! Please use a normal user and sudo!')

        env_user = getpass.getuser()
        logger.debug(f'SUDO_USER:{sudo_user!r} <-> {env_user}')
        if sudo_user != env_user:
            # Get home directory of the user that starts sudo via password database:
            import pwd  # import here to avoid issues on non-unix systems

            sudo_user_home = pwd.getpwnam(sudo_user).pw_dir
            with OverrideEnviron(HOME=sudo_user_home):
                return Path(path).expanduser()

    return Path(path).expanduser()


def backup(file_path: Path, max_try=100) -> Path:
    """
    Backup the given file, by create copy with the suffix: ".bak"
    Increment a number to the suffix -> So no old backup file will be overwritten.
    """
    assert_is_file(file_path)
    for number in range(1, max_try + 1):
        number_suffix = number if number > 1 else ''
        bak_file_candidate = file_path.with_name(f'{file_path.name}.bak{number_suffix}')
        if not bak_file_candidate.is_file():
            logger.info('Backup %s to %s', file_path, bak_file_candidate)
            shutil.copyfile(file_path, bak_file_candidate)
            return bak_file_candidate
    raise RuntimeError('No backup made: Maximum attempts to find a file name failed.')


def which(tool_name: str, mode=os.F_OK | os.X_OK, path: Path | None = None) -> Path | None:
    """
    A shutil.which() that will look into a virtualenv bin path first.
    """
    # If a virtualenv is use, check first in this bin path:
    path = path or PY_BIN_PATH
    bin_path_str = str(path)
    if bin_path_str not in os.environ['PATH']:
        if tool_path := shutil.which(tool_name, mode=mode, path=bin_path_str):
            logger.debug('%r found in: %s', tool_name, tool_path)
            return Path(tool_path)

    if tool_path := shutil.which(tool_name, mode=mode):
        logger.debug('%r found in PATH: %s', tool_name, tool_path)
        return Path(tool_path)

    logger.debug('%r not found!', tool_name)

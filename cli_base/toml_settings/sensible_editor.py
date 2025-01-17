import logging
import subprocess
import sys

from rich import print  # noqa

from cli_base.cli_tools.path_utils import which


logger = logging.getLogger(__name__)


COMMANDS = (
    'sensible-editor',
    'mcedit',
    'nano',
    'edit',
    'open',
)


def open_editor_for(file_path):
    """
    Try to open the given file in a editor.
    """
    for command in COMMANDS:
        if bin := which(command):
            logger.info('Call: "%s %s"', bin, file_path)
            try:
                return subprocess.check_call([bin, file_path])
            except subprocess.SubprocessError as err:
                print(f'Error open {file_path} with {bin}: [red]{err}')
        else:
            logger.debug(f'No "{command}" found.')

    print(f'[red]Error: No way found to open "{file_path}" !')
    print(f'(Tried: {", ".join(COMMANDS)})')
    sys.exit(1)

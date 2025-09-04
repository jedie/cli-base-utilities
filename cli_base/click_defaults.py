from pathlib import Path

import rich_click as click

from cli_base.cli_tools.verbosity import MAX_LOG_LEVEL


OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)
ARGUMENT_EXISTING_DIR = dict(
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path)
)
ARGUMENT_NOT_EXISTING_DIR = dict(
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=False,
        writable=True,
        path_type=Path,
    )
)
ARGUMENT_EXISTING_FILE = dict(
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path)
)

OPTION_KWARGS_VERBOSE = dict(  # Click tools are deprecated!
    count=True,
    type=click.IntRange(0, MAX_LOG_LEVEL),
    default=0,
    help='Verbosity level; Accepts integer value e.g.: "--verbose 2" or can be count e.g.: "-vv" ',
    show_default=True,
)

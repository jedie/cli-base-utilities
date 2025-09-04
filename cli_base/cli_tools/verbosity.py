import logging

from rich import get_console
from rich.logging import RichHandler

from cli_base.tyro_commands import TyroVerbosityArgType


MAX_LOG_LEVEL = 3


def setup_logging(*, verbosity: TyroVerbosityArgType):
    log_format = '%(message)s'
    if verbosity == 0:
        level = logging.ERROR
    elif verbosity == 1:
        level = logging.WARNING
    elif verbosity == 2:
        level = logging.INFO
    else:
        level = logging.DEBUG
        log_format = '(%(name)s) %(message)s'

    console = get_console()
    console.print(f'(Set log level {verbosity}: {logging.getLevelName(level)})', justify='right')
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt='[%x %X.%f]',
        handlers=[RichHandler(console=console, omit_repeated_times=False)],
        force=True,
    )

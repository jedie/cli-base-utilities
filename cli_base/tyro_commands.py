from collections import OrderedDict
from collections.abc import Callable
from typing import Annotated

import tyro
from tyro.conf import UseCounterAction


# https://brentyi.github.io/tyro/examples/04_additional/12_counters/
TyroVerbosityArgType = Annotated[
    UseCounterAction[int],
    tyro.conf.arg(
        aliases=['-v'],
        help='Verbosity level; e.g.: -v, -vv, -vvv, etc.',
    ),
]


class TyroCommandCli:
    """
    Helper for tyro.extras.subcommand_cli_from_dict()
    To easily register subcommands via decorator.
    See: https://github.com/brentyi/tyro/issues/139
    """

    def __init__(self):
        self.subcommands = {}

    def register(self, func: Callable) -> Callable:
        """
        Decorator to register a function as a CLI command.
        """
        func_name = func.__name__
        func_name = func_name.replace('_', '-')
        self.subcommands[func_name] = func
        return func

    def run(self, **kwargs) -> None:
        """
        Run the CLI with the registered commands.
        """
        ordered_subcommands = OrderedDict(sorted(self.subcommands.items()))
        tyro.extras.subcommand_cli_from_dict(
            subcommands=ordered_subcommands,
            **kwargs,
        )

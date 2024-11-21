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

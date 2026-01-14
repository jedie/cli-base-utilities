import sys
from pathlib import Path

import cli_base


CLI_EPILOG = 'Project Homepage: https://github.com/jedie/cli-base-utilities'

BASE_PATH = Path(cli_base.__file__).parent
PY_BIN_PATH = Path(sys.executable).parent

PY314 = sys.version_info[:2] == (3, 14)
PY313 = sys.version_info[:2] == (3, 13)
PY312 = sys.version_info[:2] == (3, 12)
PY311 = sys.version_info[:2] == (3, 11)

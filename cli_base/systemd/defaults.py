import getpass
import os
import sys
from pathlib import Path

from cli_base.constants import BASE_PATH


def get_template_path() -> Path:
    return BASE_PATH / 'systemd' / 'service_template.txt'


def get_user_name() -> str:
    user_name = os.environ.get('SUDO_USER', getpass.getuser())
    return user_name


get_user_group = get_user_name


def get_work_directory() -> Path:
    return Path().cwd()


def get_demo_exec_start() -> str:
    return f'{sys.executable} -m cli_base_app publish-loop'

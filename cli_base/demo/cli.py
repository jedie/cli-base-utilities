"""
    CLI for usage
"""

import logging
import os
import resource
import sys
import time

from rich import print  # noqa
from tyro.extras import SubcommandApp

from cli_base import __version__, constants
from cli_base.cli_tools.subprocess_utils import verbose_check_output
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.demo.settings import DemoSettings, SystemdServiceInfo
from cli_base.systemd.api import ServiceControl
from cli_base.toml_settings.api import TomlSettings
from cli_base.tyro_commands import TyroVerbosityArgType


logger = logging.getLogger(__name__)


app = SubcommandApp()


@app.command
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


######################################################################################################
SETTINGS_DIR_NAME = 'cli-base-utilities'
SETTINGS_FILE_NAME = 'cli-base-utilities-demo'


@app.command
def edit_settings(verbosity: TyroVerbosityArgType):
    """
    Edit the settings file. On first call: Create the default one.
    """
    setup_logging(verbosity=verbosity)
    TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    ).open_in_editor()


@app.command
def print_settings(verbosity: TyroVerbosityArgType):
    """
    Display (anonymized) MQTT server username and password
    """
    setup_logging(verbosity=verbosity)
    TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    ).print_settings()


######################################################################################################
# Manage systemd service commands:


@app.command
def systemd_debug(verbosity: TyroVerbosityArgType):
    """
    Print Systemd service template + context + rendered file content.
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).debug_systemd_config()


@app.command
def systemd_setup(verbosity: TyroVerbosityArgType):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).setup_and_restart_systemd_service()


@app.command
def systemd_remove(verbosity: TyroVerbosityArgType):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).remove_systemd_service()


@app.command
def systemd_status(verbosity: TyroVerbosityArgType):
    """
    Display status of systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).status()


@app.command
def systemd_logs(verbosity: TyroVerbosityArgType):
    """
    List and follow logs of systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).logs()


@app.command
def systemd_stop(verbosity: TyroVerbosityArgType):
    """
    Stops the systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    toml_settings = TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    )
    user_settings: DemoSettings = toml_settings.get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).stop()


@app.command
def demo_endless_loop(verbosity: TyroVerbosityArgType):
    """
    Just a useless example command, used in systemd DEMO: It just print some information in a endless loop.
    """
    setup_logging(verbosity=verbosity)

    # Just run a "useless" endless loop:
    wait_sec = 10
    while True:
        print('\nCLI-Base Demo endless loop\n')

        print(f'System load 1min.: {os.getloadavg()[0]}')

        usage = resource.getrusage(resource.RUSAGE_SELF)
        print(f'Time in user mode: {usage.ru_utime} sec.')
        print(f'Time in system mode: {usage.ru_stime} sec.')

        print('Wait', end='...')
        for i in range(wait_sec, 1, -1):
            time.sleep(1)
            print(i, end='...')


######################################################################################################


@app.command
def demo_verbose_check_output_error():
    """
    DEMO for a error calling cli_base.cli_tools.subprocess_utils.verbose_check_output()
    """
    verbose_check_output('python3', '-c', 'print("Just a Demo!");import sys;sys.exit(123)', exit_on_error=True)


######################################################################################################


def main():
    print(f'[bold][green]cli-base-utilities[/green] DEMO cli v[cyan]{__version__}')

    app.cli(
        prog='./demo-cli.py',
        description=constants.CLI_EPILOG,
        use_underscores=False,  # use hyphens instead of underscores
        sort_subcommands=True,
    )

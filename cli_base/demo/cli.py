"""
    CLI for usage
"""

import logging
import os
import resource
import sys
import time
from pathlib import Path

import rich_click
import rich_click as click
from rich import print  # noqa
from rich.console import Console
from rich.traceback import install as rich_traceback_install
from rich_click import RichGroup

from cli_base import __version__, constants
from cli_base.cli_tools.subprocess_utils import verbose_check_output
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from cli_base.demo.settings import DemoSettings, SystemdServiceInfo
from cli_base.systemd.api import ServiceControl
from cli_base.toml_settings.api import TomlSettings


logger = logging.getLogger(__name__)


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


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@cli.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


######################################################################################################
SETTINGS_DIR_NAME = 'cli-base-utilities'
SETTINGS_FILE_NAME = 'cli-base-utilities-demo'


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def edit_settings(verbosity: int):
    """
    Edit the settings file. On first call: Create the default one.
    """
    setup_logging(verbosity=verbosity)
    TomlSettings(
        dir_name=SETTINGS_DIR_NAME,
        file_name=SETTINGS_FILE_NAME,
        settings_dataclass=DemoSettings(),
    ).open_in_editor()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def print_settings(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_debug(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_setup(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_remove(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_status(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_stop(verbosity: int):
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


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def demo_endless_loop(verbosity: int):
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


@cli.command()
def demo_verbose_check_output_error():
    """
    DEMO for a error calling cli_base.cli_tools.subprocess_utils.verbose_check_output()
    """
    verbose_check_output('python3', '-c', 'print("Just a Demo!");import sys;sys.exit(123)', exit_on_error=True)


######################################################################################################


def main():
    print(f'[bold][green]cli-base-utilities[/green] DEMO cli v[cyan]{__version__}')

    console = Console()
    rich_traceback_install(
        width=console.size.width,  # full terminal width
        show_locals=True,
        suppress=[click, rich_click],
        max_frames=2,
    )

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()

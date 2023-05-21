import dataclasses
import logging
import os
import resource
import time

from rich import print  # noqa

from cli_base.systemd.data_classes import BaseSystemdServiceInfo, BaseSystemdServiceTemplateContext


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SystemdServiceTemplateContext(BaseSystemdServiceTemplateContext):
    """
    CLI-Base Demo - Context values for the systemd service file content.
    """

    verbose_service_name: str = 'CLI-Base Demo'


@dataclasses.dataclass
class SystemdServiceInfo(BaseSystemdServiceInfo):
    """
    CLI-Base Demo - Information for systemd helper functions.
    """

    template_context: SystemdServiceTemplateContext = dataclasses.field(default_factory=SystemdServiceTemplateContext)


@dataclasses.dataclass
class DemoSettings:
    """
    This are just settings for the "cli-base" DEMO.
    Will be used in cli_base example commands.
    See "./cli.py --help" for more information.
    """

    # Information how to setup the systemd services:
    systemd: dataclasses = dataclasses.field(default_factory=SystemdServiceInfo)


def human_wait(sec):
    print('Wait', end='...')
    for i in range(sec, 1, -1):
        time.sleep(1)
        print(i, end='...')


def endless_loop(*, user_settings: DemoSettings, verbosity: int):
    """
    Just a DEMO that will do something... ...just prints some information.
    """
    while True:
        print('\nCLI-Base Demo endless loop\n')

        print(f'System load 1min.: {os.getloadavg()[0]}')

        usage = resource.getrusage(resource.RUSAGE_SELF)
        print(f'Time in user mode: {usage.ru_utime} sec.')
        print(f'Time in system mode: {usage.ru_stime} sec.')

        human_wait(sec=10)

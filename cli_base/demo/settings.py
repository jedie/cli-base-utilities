import dataclasses

from cli_base.systemd.data_classes import BaseSystemdServiceInfo, BaseSystemdServiceTemplateContext


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
    This are just settings for the "cli-base-utilities" DEMO.
    Will be used in cli_base example commands.
    See "./cli.py --help" for more information.
    """

    # Information how to setup the systemd services:
    systemd: dataclasses = dataclasses.field(default_factory=SystemdServiceInfo)

    # Just some properties for testing:
    default_on: bool = True
    default_off: bool = False
    text: str = 'Just a String'

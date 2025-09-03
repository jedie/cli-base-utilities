import logging
from subprocess import CalledProcessError

from rich import print  # noqa
from rich.console import Console
from rich.highlighter import ReprHighlighter

from cli_base.cli_tools.rich_utils import PanelPrinter, human_error, print_code, print_unified_diff
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.systemd.data_classes import BaseSystemdServiceInfo


logger = logging.getLogger(__name__)


def exit_if_systemd_not_available(info: BaseSystemdServiceInfo):
    if not info.systemd_available:
        human_error(
            f'Systemd not available, because path not exists: {info.systemd_base_path}',
            title='[red]No Systemd',
            exit_code=1,
        )


class ServiceControl:
    """
    Manage Systemd service
    """

    def __init__(self, info: BaseSystemdServiceInfo):
        self.info = info
        self.service_name = info.service_file_path.name

    ##################################################################################################
    # Helper

    def sudo_hint_exception_exit(self, err, exit_code=1):
        human_error(
            f'{err}\n\nHint: Maybe **sudo** is needed for this command!\nTry again with sudo.',
            title='[red]Permission error',
            exception=err,
            exit_code=exit_code,
        )

    def write_service_file(self):
        print(f'Write "{self.info.service_file_path}"...')
        exit_if_systemd_not_available(self.info)

        content = self.info.get_compiled_service()
        try:
            self.info.service_file_path.write_text(content, encoding='UTF-8')
        except PermissionError as err:
            self.sudo_hint_exception_exit(err)

        self.reload_daemon(with_service_name=False)

    def remove_service_file(self):
        print(f'Remove "{self.info.service_file_path}"...')
        exit_if_systemd_not_available(self.info)

        try:
            self.info.service_file_path.unlink(missing_ok=True)
        except PermissionError as err:
            self.sudo_hint_exception_exit(err)

        self.reload_daemon(with_service_name=False)

    def service_file_is_up2date(self, print_warning: bool = True, print_diff: bool = False, console=None):
        logger.debug('Read %s...', self.info.service_file_path)
        exit_if_systemd_not_available(self.info)

        try:
            got_content = self.info.service_file_path.read_text(encoding='UTF-8')
        except PermissionError as err:
            human_error(
                title=f'[yellow]WARNING - {self.info.service_file_path}',
                message=f'Can not read the system service file, to check the content:\n{err}',
                border_style='yellow',
            )
        else:
            expect_content = self.info.get_compiled_service()
            if got_content.strip() == expect_content.strip():
                logger.info('%s is up2date, ok.', self.info.service_file_path)
                return True
            else:
                logger.warning('%s is not up2date!', self.info.service_file_path)
                if print_diff:
                    print_unified_diff(
                        txt1=expect_content,
                        txt2=got_content,
                        fromfile=str(self.info.service_file_path),
                        tofile='Fresh compiled with current settings',
                        title=f'[bright][green]unified diff[/green]: {self.info.service_file_path}',
                    )
                elif print_warning:
                    human_error(
                        title=f'[yellow]WARNING - {self.info.service_file_path}',
                        message='The systemd service file is not up2date with the current settings!',
                        border_style='yellow',
                    )
                return False

    ##################################################################################################
    # systemctl

    def call_systemctl(self, command, with_service_name=True, exit_on_error=True):
        exit_if_systemd_not_available(self.info)

        args = ['systemctl', command]
        if with_service_name:
            args.append(self.service_name)
            if not self.info.service_file_path.is_file():
                human_error(
                    f'Systemd service file not found here: {self.info.service_file_path}'
                    '\n\nHint: Setup systemd service first!',
                    title='[red]Missing systems service file',
                    exit_code=1,
                )
            else:
                self.service_file_is_up2date(print_warning=True)

        try:
            verbose_check_call(*args)
        except CalledProcessError as err:
            if exit_on_error:
                self.sudo_hint_exception_exit(err)
            raise

    def enable(self):
        self.call_systemctl('enable')

    def restart(self):
        self.call_systemctl('restart')

    def stop(self):
        self.call_systemctl('stop')

    def logs(self, follow: bool = True):
        """
        Show systemd service logs.
        """
        exit_if_systemd_not_available(self.info)
        args = ['journalctl', '-u', self.service_name]
        if follow:
            args.append('-f')
        try:
            verbose_check_call(*args)
        except CalledProcessError as err:
            self.sudo_hint_exception_exit(err)
            raise

    def reload_daemon(self, with_service_name=False):
        self.call_systemctl('daemon-reload', with_service_name=with_service_name)

    def status(self):
        try:
            self.call_systemctl('status', exit_on_error=False)
        except CalledProcessError as err:
            # Exit code is not 0 if systemd service is not running!
            human_error(
                message=(
                    'Hints:\nSystemd service is just not running, cause of a error?!\nTry to setup the services.'
                    '\nCheck your template context.'
                ),
                title=f'[bold]{err}',
                border_style='bright_yellow',
                exception=None,  # Don't print traceback
                exit_code=err.returncode,
            )

    ##################################################################################################
    # High level commands:
    def setup_and_restart_systemd_service(self):
        """
        Write Systemd service file, enable it and (re-)start the service.
        """
        self.write_service_file()
        self.enable()
        self.restart()
        self.status()

    def remove_systemd_service(self):
        self.stop()
        self.remove_service_file()

    ##################################################################################################
    # Debug

    def debug_systemd_config(
        self,
        *,
        print_diff: bool = True,
        HighlighterClass=ReprHighlighter,
        padding=(1, 5),
        console=None,
    ):
        """
        Print Systemd service template + context + rendered file content.
        """
        console = console or Console()
        pp = PanelPrinter(
            HighlighterClass=HighlighterClass,
            border_style='white',
            padding=padding,
        )
        pp.print_panel(
            content=self.info.get_template_content(),
            title=f'[magenta]Template[/magenta]: {self.info.template_path}',
        )
        pp.print_panel(
            content=self.info.get_template_context(),
            title='[cyan]Context:',
        )

        print_code(
            code=self.info.get_compiled_service(),
            lexer='ini',
            title=f'[bright][green]Compiled[/green]: {self.info.service_file_path.name}',
            console=console,
        )

        if self.info.service_file_path.is_file():
            if not print_diff:
                # Just print a warning, if service file is not up2date:
                self.service_file_is_up2date(print_warning=True)
            else:
                self.service_file_is_up2date(print_diff=True, console=console)
        else:
            logger.debug('Systemd service not created -> skip up2date check.')

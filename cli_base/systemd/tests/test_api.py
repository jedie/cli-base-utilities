import inspect
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from bx_py_utils.path import assert_is_file
from bx_py_utils.test_utils.redirect import RedirectOut
from manageprojects.test_utils.subprocess import SubprocessCallMock

from cli_base.cli_tools import path_utils
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.shutil_mocks import ShutilWhichMock
from cli_base.demo.settings import SystemdServiceInfo
from cli_base.systemd.api import ServiceControl
from cli_base.systemd.test_utils.mock_systemd_info import MockSystemdServiceInfo


def call_no_systemd_exit(func):
    with RedirectOut() as buffer:
        try:
            func()
        except SystemExit:
            assert buffer.stderr == '', f'{buffer.stderr=}'
            assert_in(
                buffer.stdout,
                parts=(
                    'No Systemd',
                    'Systemd not available',
                ),
            )
        else:
            raise AssertionError(f'No sys.exit() calling: {func.__name__=}')


class SystemdApiTestCase(TestCase):
    def test_print_systemd_file(self):
        with MockSystemdServiceInfo(
            prefix='test_print_systemd_file_', SystemdServiceInfoClass=SystemdServiceInfo
        ) as cm, RedirectOut() as buffer:
            systemd_info = cm.systemd_info
            ServiceControl(info=systemd_info).debug_systemd_config()

        self.assertEqual(buffer.stderr, '')
        assert_in(
            content=buffer.stdout,
            parts=(
                '[Unit]',
                'Description=CLI-Base Demo',
                'ExecStart=/mocked/.venv/bin/python3 -m cli_base_app publish-loop',
                'SyslogIdentifier=cli_base_demo',
            ),
        )

    def test_service_control(self):
        with MockSystemdServiceInfo(prefix='test_', SystemdServiceInfoClass=SystemdServiceInfo) as cm:
            systemd_info = cm.systemd_info
            service_control = ServiceControl(info=systemd_info)

            for func_name in ('enable', 'restart', 'stop', 'status', 'remove_systemd_service'):
                with self.subTest(func_name):
                    service_control_func = getattr(service_control, func_name)
                    with RedirectOut() as buffer, self.assertRaises(SystemExit):
                        service_control_func()
                    assert_in(
                        content=buffer.stdout,
                        parts=(
                            'Systemd service file not found',
                            'Hint: Setup systemd service first!',
                        ),
                    )

            with (
                SubprocessCallMock() as mock,
                patch.object(path_utils, 'shutil', ShutilWhichMock(command_map={'systemctl': '/usr/bin/systemctl'})),
                RedirectOut() as buffer,
            ):
                service_control.setup_and_restart_systemd_service()

            assert_in(
                content=buffer.stdout,
                parts=(
                    f'Write "{systemd_info.service_file_path}"...',
                    'systemctl daemon-reload',
                    'systemctl enable cli_base_demo.service',
                    'systemctl restart cli_base_demo.service',
                    'systemctl status cli_base_demo.service',
                ),
            )
            assert_is_file(systemd_info.service_file_path)

            self.assertEqual(
                mock.get_popenargs(),
                [
                    ['/usr/bin/systemctl', 'daemon-reload'],
                    ['/usr/bin/systemctl', 'enable', 'cli_base_demo.service'],
                    ['/usr/bin/systemctl', 'restart', 'cli_base_demo.service'],
                    ['/usr/bin/systemctl', 'status', 'cli_base_demo.service'],
                ],
            )

    def test_no_systemd(self):
        info = SystemdServiceInfo(systemd_base_path=Path('/no/systemd/on/this/system'))
        service_control = ServiceControl(info=info)

        functions = []
        for name, func in inspect.getmembers(service_control, predicate=inspect.ismethod):
            if name in ('__init__', 'call_systemctl', 'debug_systemd_config', 'sudo_hint_exception_exit'):
                continue
            call_no_systemd_exit(func)
            functions.append(name)
        self.assertEqual(
            sorted(functions),
            [
                'enable',
                'logs',
                'reload_daemon',
                'remove_service_file',
                'remove_systemd_service',
                'restart',
                'service_file_is_up2date',
                'setup_and_restart_systemd_service',
                'status',
                'stop',
                'write_service_file',
            ],
        )

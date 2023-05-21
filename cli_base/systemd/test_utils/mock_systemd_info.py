import shutil
from unittest import mock

from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.test_utils.context_managers import MassContextManager

from cli_base.cli_tools.test_utils.environment_fixtures import MockCurrentWorkDir
from cli_base.systemd import defaults
from cli_base.systemd.data_classes import BaseSystemdServiceInfo


class MockedSys:
    executable = '/mocked/.venv/bin/python3'


class MockSystemdServiceInfo(MassContextManager):
    """
    Set all values in cli_base/systemd/defaults.py to static ones,
    independent of current user/environment.

    So that creating a SystemdServiceInfo() instance will result in a well known state.

    Note: The work_dir has still a random suffix!
    """

    def __init__(self, *, prefix: str, SystemdServiceInfoClass):
        self.mocked_cwd = MockCurrentWorkDir(prefix=prefix)
        assert issubclass(SystemdServiceInfoClass, BaseSystemdServiceInfo), f'{SystemdServiceInfoClass=}'
        self.SystemdServiceInfoClass = SystemdServiceInfoClass

        self.mocks = (
            self.mocked_cwd,
            OverrideEnviron(SUDO_USER='MockedUserName'),
            mock.patch.object(defaults, 'sys', MockedSys()),
        )

        self.temp_path = None
        self.systemd_info = None

    def __enter__(self) -> 'MockSystemdServiceInfo':
        super().__enter__()
        self.temp_path = self.mocked_cwd.temp_path
        mocked_systemd_base_path = self.temp_path / 'etc-systemd-system'
        mocked_systemd_base_path.mkdir()
        self.systemd_info: BaseSystemdServiceInfo = self.SystemdServiceInfoClass(
            systemd_base_path=mocked_systemd_base_path  # noqa
        )

        # Move the source template into temp directory:
        src_template_path = self.systemd_info.template_path
        dst_template_path = self.temp_path / src_template_path.name
        shutil.copyfile(src_template_path, dst_template_path)
        self.systemd_info.template_path = dst_template_path

        return self

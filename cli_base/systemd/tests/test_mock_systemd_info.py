import dataclasses
from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_dir, assert_is_file
from bx_py_utils.test_utils.snapshot import assert_text_snapshot

from cli_base.cli_tools.dict_utils import replace_dict_values_prefix
from cli_base.systemd.data_classes import BaseSystemdServiceInfo, BaseSystemdServiceTemplateContext
from cli_base.systemd.test_utils.mock_systemd_info import MockSystemdServiceInfo
from cli_base.toml_settings.serialize import dataclass2toml_str
from cli_base.toml_settings.test_utils.data_class_utils import replace_dataclass_values


@dataclasses.dataclass
class SystemdServiceTemplateContext(BaseSystemdServiceTemplateContext):
    """Systemd template context - Test dataclass"""

    verbose_service_name: str = 'Service Info Mock Test'


@dataclasses.dataclass
class TestSystemdServiceInfo(BaseSystemdServiceInfo):
    """Systemd service info - Test dataclass"""

    template_context: SystemdServiceTemplateContext = dataclasses.field(default_factory=SystemdServiceTemplateContext)


class MocksTest(TestCase):
    def test_mock(self):
        with MockSystemdServiceInfo(prefix='test_mock', SystemdServiceInfoClass=TestSystemdServiceInfo) as cm:
            self.assertIsInstance(cm, MockSystemdServiceInfo)

            temp_path = cm.temp_path
            self.assertIsInstance(temp_path, Path)
            self.assertEqual(temp_path, Path.cwd())
            assert_is_dir(temp_path)

            systemd_info = cm.systemd_info
            self.assertIsInstance(systemd_info, TestSystemdServiceInfo)

            # Check some samples:
            self.assertEqual(systemd_info.template_context.verbose_service_name, 'Service Info Mock Test')
            self.assertEqual(systemd_info.template_context.user, 'MockedUserName')
            self.assertEqual(systemd_info.template_context.group, 'MockedUserName')
            self.assertEqual(
                systemd_info.template_context.exec_start, '/mocked/.venv/bin/python3 -m cli_base_app publish-loop'
            )
            self.assertEqual(systemd_info.service_slug, 'service_info_mock_test')
            assert_is_file(systemd_info.template_path)

            data = dataclasses.asdict(systemd_info)

            # Replace the random temp path:
            replace_dict_values_prefix(data, prefix=str(temp_path), new_prefix='/mocked-temp-path/')

            # Check some samples, again:
            self.assertEqual(data['template_path'], Path('/mocked-temp-path/service_template.txt'))
            self.assertEqual(
                data['service_file_path'], Path('/mocked-temp-path/etc-systemd-system/service_info_mock_test.service')
            )

            # Replace the random temp path in dataclass instance:
            replace_dataclass_values(systemd_info, data=data)

            doc_str = dataclass2toml_str(systemd_info)
            assert_text_snapshot(got=doc_str, extension='.toml')

        self.assertFalse(temp_path.exists())

import dataclasses
from pathlib import Path

from bx_py_utils.environ import OverrideEnviron

from cli_base.cli_tools.test_utils.environment_fixtures import MockCurrentWorkDir
from cli_base.toml_settings.api import TomlSettings
from cli_base.toml_settings.serialize import dataclass2toml_str


def replace_dataclass_values(instance, *, data: dict):
    """
    Replace dataclass values in-place with values from given dict.
    """
    assert dataclasses.is_dataclass(instance), f'{instance=}'

    for key, value in data.items():
        if isinstance(value, dict):
            sub_dataclass = getattr(instance, key)
            replace_dataclass_values(sub_dataclass, data=value)
        else:
            assert hasattr(instance, key), f'Attribute "{key}" missing on: {instance=}'
            setattr(instance, key, value)


def replace_path_values(instance):
    assert dataclasses.is_dataclass(instance), f'{instance=}'

    data = dataclasses.asdict(instance)
    for key, value in data.items():
        if isinstance(value, dict):
            sub_dataclass = getattr(instance, key)
            replace_path_values(sub_dataclass)
        elif isinstance(value, Path):
            setattr(instance, key, str(value))


class MockTomlSettings(MockCurrentWorkDir):
    """
    Mock TomlSettings with overwrites of settings dataclass instance.
    Will create a "default" settings.toml in a temporary directory.
    """

    def __init__(
        self,
        *,
        SettingsDataclass,
        settings_overwrites: dict,  # Change values in SettingsDataclass instance
        dir_name='mocked_dir_name',
        file_name='mocked_file_name',
        **temp_kwargs,
    ):
        super().__init__(**temp_kwargs)

        assert dataclasses.is_dataclass(SettingsDataclass), f'{SettingsDataclass=}'
        self.SettingsDataclass = SettingsDataclass
        self.settings_overwrites = settings_overwrites
        self.dir_name = dir_name
        self.file_name = file_name

        self.overwrite_env = None
        self.toml_settings = None
        self.settings_dataclass = None

    def __enter__(self) -> 'MockTomlSettings':
        super().__enter__()

        self.overwrite_env = OverrideEnviron(HOME=str(self.temp_path))
        self.overwrite_env.__enter__()

        self.config_path = self.temp_path / '.config'
        self.config_path.mkdir()

        self.settings_dataclass = self.SettingsDataclass()
        replace_dataclass_values(instance=self.settings_dataclass, data=self.settings_overwrites)

        self.toml_settings = TomlSettings(
            dir_name=self.dir_name,
            file_name=self.file_name,
            settings_dataclass=self.settings_dataclass,
        )

        doc_str = dataclass2toml_str(instance=self.settings_dataclass)
        self.toml_settings.file_path.write_text(doc_str, encoding='UTF-8')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.overwrite_env.__exit__(exc_type, exc_val, exc_tb)
        if exc_type:
            return False

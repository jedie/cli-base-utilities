from cli_base.cli_tools.test_utils.rich_test_utils import BASE_WIDTH, NoColorEnvRich
from cli_base.toml_settings.test_utils.data_class_utils import MockTomlSettings


class TomlSettingsCliMock(NoColorEnvRich):
    """
    IMPORTANT: We must ensure that no local user settings added to the help text
    So we can't directly invoke_click() here, because user settings are read and
    used on module level!
    So we must use subprocess and use a default settings file!
    """

    def __init__(
        self,
        *,
        SettingsDataclass,
        settings_overwrites: dict,  # Change values in SettingsDataclass instance
        dir_name='mocked_dir_name',
        file_name='mocked_file_name',
        prefix='test_mock',  # Temp dir prefix
        width: int = BASE_WIDTH,  # Terminal max width
    ):
        super().__init__(width)
        self.mocks += [
            MockTomlSettings(
                SettingsDataclass=SettingsDataclass,
                settings_overwrites=settings_overwrites,
                dir_name=dir_name,
                file_name=file_name,
                prefix=prefix,
            ),
        ]

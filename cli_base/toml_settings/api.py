import dataclasses
import logging
from collections.abc import Iterable
from pathlib import Path

import tomlkit
from rich import print  # noqa
from rich.console import Console
from tomlkit import TOMLDocument

from cli_base.cli_tools.path_utils import backup, expand_user
from cli_base.cli_tools.rich_utils import human_error
from cli_base.toml_settings.debug import print_dataclasses
from cli_base.toml_settings.deserialize import toml2dataclass
from cli_base.toml_settings.exceptions import UserSettingsNotFound
from cli_base.toml_settings.sensible_editor import open_editor_for
from cli_base.toml_settings.serialize import dataclass2toml_str


logger = logging.getLogger(__name__)


class TomlSettings:
    settings_directories = (  # Path candidates where setting files will be stored
        '~/.config/',
        '~',
    )

    # Print this error message if settings file not exists:
    not_exists_hint = 'No settings created yet: (Hint: call "edit-settings" first!)'

    def __init__(
        self,
        *,
        dir_name: str,
        file_name: str,
        settings_dataclass: dataclasses,
        not_exist_exit_code=-1,
    ):
        self.file_path = self.get_settings_file_path(dir_name, file_name)

        assert dataclasses.is_dataclass(settings_dataclass), f'No dataclass: {settings_dataclass}'
        self.settings_dataclass = settings_dataclass
        self.not_exist_exit_code = not_exist_exit_code

    def get_settings_path(self) -> Path:
        candidates = []
        for candidate in self.settings_directories:
            if path := expand_user(Path(candidate)):  # Expand with user home, even if called via sudo!
                candidates.append(path)
                if path.is_dir():
                    return path
        raise RuntimeError(f'All settings directories does not exists! Tried: {candidates}')

    def get_settings_file_path(self, dir_name: str, file_name: str) -> Path:
        assert dir_name == Path(dir_name).stem, f'Invalid {dir_name=!r}'
        assert file_name == Path(file_name).stem, f'Invalid {file_name=!r}'
        settings_path = self.get_settings_path() / dir_name
        if not settings_path.exists():
            settings_path.mkdir(parents=False, exist_ok=False)
        return settings_path / f'{file_name}.toml'

    def open_in_editor(self) -> None:
        if not self.file_path.is_file():
            logger.info('Settings file "%s" not exist -> create default', self.file_path)
            doc_str = dataclass2toml_str(instance=self.settings_dataclass)
            self.file_path.write_text(doc_str, encoding='UTF-8')

        open_editor_for(self.file_path)

    def get_user_settings(self, *, debug: bool = False) -> dataclasses:
        if debug:
            print(f'Use user settings file: {self.file_path}', end='...')
        if not self.file_path.is_file():
            human_error(message=self.not_exists_hint, exit_code=self.not_exist_exit_code)
            raise UserSettingsNotFound(self.file_path)

        doc_str = self.file_path.read_text(encoding='UTF-8')
        user_settings_doc: TOMLDocument = tomlkit.loads(doc_str)
        logger.debug(f'Loaded settings: {user_settings_doc=}')

        document_changed = toml2dataclass(document=user_settings_doc, instance=self.settings_dataclass)
        logger.debug(f'{document_changed=}')
        if document_changed:
            logger.info('User toml file needs update!')
            doc_str = tomlkit.dumps(user_settings_doc, sort_keys=False)
            backup(self.file_path)
            self.file_path.write_text(doc_str, encoding='UTF-8')

        if debug:
            print('[green]read, ok.')
        return self.settings_dataclass

    def print_settings(self, *, anonymize_keys: Iterable = ('password', 'email')) -> None:
        """
        Print (anonymized) settings
        """
        user_settings = self.get_user_settings(debug=True)

        print()
        console = Console()
        console.rule(f'User settings: {self.file_path}')
        anonymized = print_dataclasses(instance=user_settings, anonymize_keys=anonymize_keys)
        if anonymized:
            info = f'(anonymize keys: {", ".join(sorted(anonymized))})'
        else:
            info = None
        console.rule(info)

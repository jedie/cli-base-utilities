from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file


class AssertCliHelpInReadme:
    README_FILE_NAME = 'README.md'

    def __init__(self, *, base_path: Path, cli_epilog: str):
        self.readme_path = base_path / self.README_FILE_NAME
        assert_is_file(self.readme_path)

        self.cli_epilog = cli_epilog

    def assert_block(self, text_block: str, marker: str):
        if self.cli_epilog:
            text_block = text_block.replace(self.cli_epilog, '')

        text_block = f'```\n{text_block.strip()}\n```'
        assert_readme_block(
            readme_path=self.readme_path,
            text_block=text_block,
            start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
            end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
        )

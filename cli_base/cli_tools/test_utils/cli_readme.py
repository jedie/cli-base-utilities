from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file


def assert_cli_help_in_readme(*, readme_path: Path, text_block: str, marker: str, cli_epilog: str = ''):
    assert_is_file(readme_path)

    if cli_epilog:
        text_block = text_block.replace(cli_epilog, '')

    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=readme_path,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )

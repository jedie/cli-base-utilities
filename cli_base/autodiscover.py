from importlib import import_module
from pathlib import Path

from bx_py_utils.path import assert_is_file


def import_all_files(*, package: str, init_file: str) -> list:
    """
    Just import all python files in the same directory than caller.
    Needful if a registry is used via imports.
    """
    init_file_path = Path(init_file)
    assert_is_file(init_file_path)

    module_path = init_file_path.parent

    imported_names = []
    for item in module_path.glob('*.py'):
        file_name = item.stem
        if file_name.startswith('_'):
            continue

        name = f'{package}.{file_name}'
        import_module(name)
        imported_names.append(name)
    return imported_names

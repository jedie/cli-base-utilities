import logging
from pathlib import Path

from rich import print

from cli_base.cli_tools.git import Git


logger = logging.getLogger(__name__)


def _print_version(
    module,
    project_root: Path | None = None,
    project_name: str | None = None,
):
    if not project_name:
        project_name = module.__name__.replace('_', '-')
    print(f'[bold][green]{project_name}[/green] v', end='')
    print(module.__version__, end=' ')

    if not project_root:
        project_root = Path(module.__file__).parent.parent
    git_path = project_root / '.git'
    if git_path.is_dir():
        git = Git(cwd=git_path)
        current_hash = git.get_current_hash(verbose=False)
        print(f'[blue]{current_hash}[/blue]', end=' ')
        print(f'([white]{git.cwd}[/white])')
    else:
        print(f'(No git found for: {project_root})')


def print_version(
    module,
    project_root: Path | None = None,
    project_name: str | None = None,
) -> None:
    try:
        _print_version(module=module, project_root=project_root, project_name=project_name)
    except Exception as err:
        logger.exception('Error print version')

        # Catch all errors, otherwise the CLI is not usable ;)
        print(f'{module} (print version error: {err})')

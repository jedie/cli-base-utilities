"""
DocWrite: shell_completion.md # Tyro CLI Shell Completion
Helper to setup shell completion for a Tyro based CLI program.
"""

import logging
import os
import re
import sys
import textwrap
from pathlib import Path

from rich import print  # noqa

from cli_base.cli_tools.subprocess_utils import verbose_check_output


logger = logging.getLogger(__name__)
TYRO_WRITE_COMPLETION_ARG = '--tyro-write-completion'


def append_file(file_path: Path, content: str) -> bool:
    if file_path.exists():
        with file_path.open('r') as f:
            if content in f.read():
                logger.debug('Content already exists in %s', file_path)
                return False

    logger.debug('Add content to %s', file_path)
    with file_path.open('a') as f:
        f.write(content)
    logger.info('Append content to %s', file_path)
    return True


def get_bash_completions_path() -> Path:
    # See: https://github.com/scop/bash-completion/blob/main/README.md#faq
    paths = (
        Path(os.environ.get('BASH_COMPLETION_USER_DIR', '')) / 'completions',
        Path(os.environ.get('XDG_DATA_HOME', '')) / 'bash-completion' / 'completions',
    )
    for path in paths:
        if path.is_dir():
            return path

    return Path.home() / '.local' / 'share' / 'bash-completion' / 'completions'


def setup_bash_completion(prog_name: str, remove: bool = False) -> None:
    """
    DocWrite: shell_completion.md # Tyro CLI Shell Completion
    Supports Bash shell
    """
    print(
        f'\nSetting up [blue]Bash[/blue] completion for {prog_name} ...',
    )

    bash_completions_path = get_bash_completions_path()
    completion_file_path = bash_completions_path / f'{prog_name}.sh'

    if path := os.environ.get('BASH_COMPLETION_USER_FILE'):
        bash_user_completion_file = Path(path)
    else:
        bash_user_completion_file = Path.home() / '.bash_completion'

    bash_user_completion_content = textwrap.dedent(f"""
        # Added by {__file__} for {prog_name}:
        source "{completion_file_path}"
    """)

    if remove:
        if completion_file_path.exists():
            logger.info('Removing completion script %s', completion_file_path)
            completion_file_path.unlink()
            print(f'[green]Removed bash completion {completion_file_path}[/green]')
        else:
            logger.warning('Completion script %s does not exist, nothing to remove.', completion_file_path)
        if bash_user_completion_file.exists():
            logger.info('Removing lines from %s', bash_user_completion_file)
            old_content = bash_user_completion_file.read_text()
            new_content = re.sub(bash_user_completion_content, '', old_content, flags=re.IGNORECASE | re.DOTALL)
            if old_content == new_content:
                print(f'[yellow]Error: Content not found in {bash_user_completion_file}[/yellow]')
            else:
                bash_user_completion_file.write_text(new_content)
                print(f'[green]Cleaned {bash_user_completion_file}[/green]')
        return

    # Setup bash completion:

    completion_file_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info('Writing completion script to %s', completion_file_path)
    verbose_check_output(
        sys.argv[0],
        TYRO_WRITE_COMPLETION_ARG,
        'bash',
        completion_file_path,
        verbose=False,
    )
    print(f'[green]Wrote bash completion script to: {completion_file_path}')

    # Write into e.g.:
    #   ~/.local/share/bash-completion/completions/foo_bar.sh
    # Is not the only needed step, because the bash-completion package doesn't source this!
    # See "Lookup order" in:
    #   https://github.com/scop/bash-completion/blob/main/bash_completion
    # The only sourced user completion file is:
    #   ~/.bash_completion
    # So add a line to source our completion file there:

    append = append_file(
        bash_user_completion_file,
        content=bash_user_completion_content,
    )
    if append:
        print(f'[green]Append completion script to: {bash_user_completion_file}')
    else:
        print(f'[yellow]Completion script already sourced in: {bash_user_completion_file}')


def setup_zshell_completion(prog_name: str, remove: bool = False) -> None:
    """
    DocWrite: shell_completion.md # Tyro CLI Shell Completion
    Supports Z-Shell
    """
    print(
        f'\nSetting up [blue]Z-Shell[/blue] completion for {prog_name} ...',
    )
    zsh_completions_file_path = Path.home() / '.zfunc' / f'_{prog_name}.zsh'
    if remove:
        if zsh_completions_file_path.exists():
            logger.info('Removing completion script %s', zsh_completions_file_path)
            zsh_completions_file_path.unlink()
            print(f'[green]Removed zsh completion {zsh_completions_file_path}[/green]')
        else:
            logger.warning('Completion script %s does not exist, nothing to remove.', zsh_completions_file_path)
        return

    # Setup zsh completion:

    zsh_completions_file_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info('Writing completion script to %s', zsh_completions_file_path)
    verbose_check_output(
        sys.argv[0],
        TYRO_WRITE_COMPLETION_ARG,
        'zsh',
        zsh_completions_file_path,
        verbose=False,
    )
    print(f'[green]Wrote zsh completion script to: {zsh_completions_file_path}')


def setup_tyro_shell_completion(prog_name: str, remove: bool = False) -> None:
    """
    DocWrite: shell_completion.md # Tyro CLI Shell Completion
    Usage: Expand you Tyro CLI and call `setup_tyro_shell_completion()` from your program ;)
    """
    print(f'\nSetting up shell completion for [bold]{prog_name}[/bold] ...\n')

    setup_bash_completion(prog_name, remove)
    setup_zshell_completion(prog_name, remove)

    print('You may need to restart your shell ;)')

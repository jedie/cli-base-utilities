from __future__ import annotations

import importlib
import os
import re
from collections.abc import Iterable
from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from bx_py_utils.pyproject_toml import get_pyproject_config
from packaging.version import Version
from rich import print  # noqa

from cli_base.cli_tools.git import Git, GitHistoryEntry, GithubInfo, GitlabInfo


def clean_text(text: str) -> str:
    """
    Clean the text via regex and remove all non-ascii chars and lower it.
    >>> clean_text('A ÄÖÜ äöüß Test Message 123!')
    'a test message 123'
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', ' ', text)  # Remove all non-ascii chars
    text = re.sub(r' +', ' ', text)  # Remove double spaces
    return text.strip()


class TagHistoryRenderer:
    def __init__(
        self,
        *,
        current_version: str,
        skip_prefixes: tuple[str, ...],
        project_info: GithubInfo | GitlabInfo,
        main_branch_name: str = 'main',
        add_author: bool = True,
        collapse_after: int | None = 4,
        collapse_marker: str = 'Expand older history entries ...',
    ):
        self.current_version = Version(current_version)
        self.skip_prefixes = [txt.lower() for txt in skip_prefixes]
        self.project_info = project_info

        self.main_branch_name = main_branch_name
        self.add_author = add_author
        self.collapse_after = collapse_after
        self.collapse_marker = collapse_marker

        self.base_url = None  # Must be set in child class!

    def version2str(self, version: Version):
        return f'v{version}'

    def skip(self, comment) -> bool:
        comment = comment.lower()
        for skip_prefix in self.skip_prefixes:
            if comment.startswith(skip_prefix):
                return True
        return False

    @classmethod
    def clean_log_comment(cls, comment: str) -> str:
        """
        GitHub may add suffixes like "(#123)" to the commit message.
        We remove them here, e.g.:
        >>> TagHistoryRenderer.clean_log_comment('Fix a problem (#123)')
        'Fix a problem'
        >>> TagHistoryRenderer.clean_log_comment('A commit. (fixed #456)')
        'A commit. (fixed #456)'
        """
        comment = re.sub(r'\s*\(\#\d+\)\s*$', '', comment)  # Remove "(#123)" at the end
        return comment

    def render(self, tags_history: list[GitHistoryEntry]) -> Iterable[str]:
        collapsed = False
        for count, entry in enumerate(tags_history):
            if self.collapse_after and count == self.collapse_after:
                yield f'\n<details><summary>{self.collapse_marker}</summary>\n'
                collapsed = True

            if entry.last == 'HEAD':
                version: Version = entry.tag.version

                release_planing = self.current_version > version
                if release_planing:
                    new_version = self.version2str(self.current_version)
                    compare_url = self.project_info.compare_url(old=entry.next, new=new_version)
                    yield f'* [{new_version}]({compare_url})'
                else:
                    compare_url = self.project_info.compare_url(old=entry.next, new=self.main_branch_name)
                    yield f'* [**dev**]({compare_url})'
            else:
                compare_url = self.project_info.compare_url(old=entry.next, new=entry.last)
                yield f'* [{entry.last}]({compare_url})'

            seen_comments = set()
            for log_line in entry.log_lines:
                if self.skip(log_line.comment):
                    continue

                commit_comment = self.clean_log_comment(log_line.comment)

                # Remove duplicate git commits, e.g.: several "update requirements" commits ;)
                cleaned_comment = clean_text(commit_comment)
                if cleaned_comment in seen_comments:
                    continue
                seen_comments.add(cleaned_comment)

                if self.add_author:
                    author = f' {log_line.author}'
                else:
                    author = ''
                yield f'  * {log_line.date.isoformat()}{author} - {commit_comment}'

        if collapsed:
            yield '\n</details>\n'


def get_git_history(
    *,
    git: Git,
    current_version: str,
    add_author: bool = True,
    skip_prefixes: tuple[str, ...] = ('Release as', 'Prepare release'),
    verbose: bool = False,
) -> Iterable[str]:
    """
    Generate a project history base on git commits/tags.
    """
    main_branch_name = git.get_main_branch_name(verbose=False)
    project_info = git.get_project_info(verbose=False)
    if project_info:
        tags_history: list[GitHistoryEntry] = git.get_tag_history(verbose=verbose)
        renderer = TagHistoryRenderer(
            current_version=current_version,
            skip_prefixes=skip_prefixes,
            project_info=project_info,
            main_branch_name=main_branch_name,
            add_author=add_author,
        )
        yield from renderer.render(tags_history)


def update_readme_history(
    *,
    base_path: Path | None = None,
    verbosity: int = 0,
    raise_update_error: bool = False,
) -> bool:
    """
    Update project history base on git commits/tags in README.md

    Callable via CLI e.g.:

        python -m cli_base update-readme-history -v

    The `pyproject.toml` must contain a section like this:

        [tool.cli_base]
        version_module_name = "cli_base"

    The `README.md` must contain these markers:

        [comment]: <> (✂✂✂ auto generated history start ✂✂✂)
        [comment]: <> (✂✂✂ auto generated history end ✂✂✂)
    """
    git: Git = Git(cwd=base_path, detect_root=True)
    base_path = git.cwd
    if verbosity > 2:
        print(f'{base_path=}')

    pyproject_toml_path = base_path / 'pyproject.toml'
    if verbosity > 1:
        print(f'{pyproject_toml_path=}')
    assert_is_file(pyproject_toml_path)

    readme_md_path = base_path / 'README.md'
    if verbosity > 1:
        print(f'{readme_md_path=}')
    assert_is_file(readme_md_path)

    version_module_name: str = get_pyproject_config(
        section=('tool', 'cli_base', 'version_module_name'),
        base_path=pyproject_toml_path.parent,
    )
    if not version_module_name:
        raise LookupError(f'No "tool.cli_base.version_module_name" in {pyproject_toml_path}')
    elif verbosity > 1:
        print(f'{version_module_name=}')

    module = importlib.import_module(version_module_name)
    current_version = module.__version__
    assert current_version, f'No version found for {version_module_name}'

    if verbosity > 1:
        print(f'{current_version=}')

    git = Git()
    git_history = get_git_history(
        git=git,
        current_version=current_version,
        add_author=False,
        verbose=verbosity > 1,
    )
    history = '\n'.join(git_history)

    old_mtime = readme_md_path.stat().st_mtime
    try:
        assert_readme_block(
            readme_path=readme_md_path,
            text_block=f'\n{history}\n',
            start_marker_line='[comment]: <> (✂✂✂ auto generated history start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated history end ✂✂✂)',
        )
    except AssertionError:
        if raise_update_error:
            raise

        new_mtime = readme_md_path.stat().st_mtime
        if new_mtime > old_mtime:
            print(f'History in {readme_md_path} updated.')
            git.add(readme_md_path)
            return True
        else:
            raise
    else:
        print(f'History in {readme_md_path} is up-to-date.')
        return False


if __name__ == '__main__':
    from cli_base import __version__

    git = Git()
    git_history = get_git_history(git=git, current_version=__version__)
    for line in git_history:
        print(line)

    from cli_base.cli_dev import PACKAGE_ROOT

    os.chdir(PACKAGE_ROOT)

    update_readme_history(verbosity=2)

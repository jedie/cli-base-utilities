from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from cli_base.cli_tools.git import Git, GitHistoryEntry, GithubInfo, GitlabInfo, get_git


class TagHistoryRenderer:
    def __init__(
        self,
        *,
        project_info: GithubInfo | GitlabInfo,
        main_branch_name: str = 'main',
        add_author: bool = True,
    ):
        self.project_info = project_info

        self.main_branch_name = main_branch_name
        self.add_author = add_author

        self.base_url = None  # Must be set in child class!

    def render(self, tags_history: list[GitHistoryEntry]) -> Iterable[str]:
        for entry in tags_history:
            if entry.last == 'HEAD':
                compare_url = self.project_info.compare_url(old=entry.next, new=self.main_branch_name)
                yield f'* [**dev**]({compare_url})'
                add_commit_url = False
            else:
                compare_url = self.project_info.compare_url(old=entry.next, new=entry.last)
                yield f'* [{entry.last}]({compare_url})'
                add_commit_url = True

            for log_line in entry.log_lines:
                if self.add_author:
                    author = f' {log_line.author}'
                else:
                    author = ''
                if add_commit_url:
                    commit_url = self.project_info.commit_url(hash=log_line.hash)
                    yield f'  * [{log_line.date.isoformat()}{author}]({commit_url}) - {log_line.comment}'
                else:
                    yield f'  * {log_line.date.isoformat()}{author} - {log_line.comment}'

            if entry.last == 'HEAD':
                yield '  * tbc'


def get_git_history(cwd: Path | None = None, add_author: bool = True, verbose: bool = False) -> Iterable[str]:
    """
    Generate a project history base on git commits/tags.
    """
    git: Git = get_git(cwd=cwd)
    main_branch_name = git.get_main_branch_name(verbose=False)
    project_info = git.get_project_info(verbose=False)
    if project_info:
        tags_history: list[GitHistoryEntry] = git.get_tag_history(verbose=verbose)
        renderer = TagHistoryRenderer(
            project_info=project_info,
            main_branch_name=main_branch_name,
            add_author=add_author,
        )
        yield from renderer.render(tags_history)


if __name__ == '__main__':
    for line in get_git_history():
        print(line)

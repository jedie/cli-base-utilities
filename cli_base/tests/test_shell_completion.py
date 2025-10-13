import re
from pathlib import Path
from unittest import TestCase

from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.path import assert_is_file

from cli_base.cli_dev import PACKAGE_ROOT
from cli_base.cli_tools.subprocess_utils import verbose_check_output


def patch_file_content(file_path: Path, source: str, target: str) -> int:
    """
    Replace all occurrences of `source` with `target` in the given file.
    returns the number of replacements made.
    """
    assert_is_file(file_path)
    content = file_path.read_text()
    content, count = re.subn(re.escape(source), target, content)
    if count > 0:
        print(f'{count=} replacement of {source=} ')
        file_path.write_text(content)
    return count


class ShellCompleteTestCase(TestCase):
    def test_happy_path(self):
        snapshot_path = Path(__file__).parent / 'shell_complete_snapshots'

        completion_user_file_path = snapshot_path / '.bash_completion'
        if completion_user_file_path.exists():
            # The content will be appended, because match detection doesn't work
            # because of replaced paths. So just remove the file. To recreation
            # is tested below.
            completion_user_file_path.unlink()

        with OverrideEnviron(HOME=str(snapshot_path)):
            verbose_check_output(PACKAGE_ROOT / 'dev-cli.py', 'shell-completion')
            verbose_check_output(PACKAGE_ROOT / 'cli.py', 'shell-completion')

        self.assertEqual(
            patch_file_content(
                file_path=snapshot_path / '.bash_completion',
                source=str(snapshot_path),
                target='{HOME}',
            ),
            2,
        )
        cwd_str = str(PACKAGE_ROOT)
        self.assertEqual(
            patch_file_content(
                file_path=snapshot_path / '.bash_completion',
                source=cwd_str,
                target='{CWD}',
            ),
            2,
        )
        for file_path in (
            snapshot_path / '.local/share/bash-completion/completions/cli_base_utilities_app_cli.sh',
            snapshot_path / '.local/share/bash-completion/completions/cli_base_utilities_dev_cli.sh',
            snapshot_path / '.zfunc/_cli_base_utilities_app_cli.zsh',
            snapshot_path / '.zfunc/_cli_base_utilities_dev_cli.zsh',
        ):
            assert_is_file(file_path)

import shlex
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from pre_commit import clientlib

from cli_base.cli.dev import PACKAGE_ROOT
from cli_base.cli_tools.subprocess_utils import ToolsExecutor


class PreCommitTests(TestCase):
    def test_pre_commit_hooks_file(self):
        file_path = PACKAGE_ROOT / '.pre-commit-hooks.yaml'
        assert_is_file(file_path)

        hooks = clientlib.load_manifest(file_path)

        tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)

        checked_ids = []
        for hook in hooks:
            entry = hook['entry']
            popenargs = shlex.split(entry)
            tools_executor.verbose_check_call(*popenargs)
            checked_ids.append(hook['id'])

        checked_ids.sort()
        self.assertEqual(checked_ids, ['update-readme-history'])

    def test_pre_commit_config_file(self):
        file_path = PACKAGE_ROOT / '.pre-commit-config.yaml'
        assert_is_file(file_path)

        clientlib.load_config(file_path)

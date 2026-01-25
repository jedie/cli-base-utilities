import getpass
import os
import shlex
import sys
import tempfile
from pathlib import Path

from bx_py_utils.environ import OverrideEnviron


class AsSudoCallOverrideEnviron(OverrideEnviron):
    """
    Manipulate the environment variables so it looks like a "sudo" call.
    Compare with: "sudo env | sort" ;)
    """

    def __init__(self, **overrides):
        overrides = {
            'SUDO_COMMAND': shlex.join(sys.argv),
            'SUDO_UID': str(os.getuid()),
            'SUDO_GID': str(os.getgid()),
            'SUDO_USER': getpass.getuser(),
            'LOGNAME': 'root',
            'HOME': '/root',
            **overrides,
        }
        super().__init__(**overrides)


class MockCurrentWorkDir(tempfile.TemporaryDirectory):
    """
    Context Manager to move the "CWD" to a temp directory.
    """

    def __init__(self, **kwargs):
        self.old_cwd = Path().cwd()
        super().__init__(**kwargs)

    def __enter__(self):
        temp_dir = super().__enter__()
        os.chdir(temp_dir)
        self.temp_path = Path(temp_dir).resolve()  # Resolve needed e.g.: under macos
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)
        super().__exit__(exc_type, exc_val, exc_tb)
        if exc_type:
            return False

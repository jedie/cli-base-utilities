import getpass
import os
from pathlib import Path
from unittest import TestCase

from cli_base.cli_tools.test_utils.environment_fixtures import AsSudoCallOverrideEnviron


class EnvironFixturesTestCase(TestCase):
    def test_happy_path(self):
        user_id = os.getuid()
        user_group_id = os.getgid()

        with AsSudoCallOverrideEnviron():
            self.assertEqual(getpass.getuser(), 'root')
            self.assertEqual(Path().home(), Path('/root'))
            self.assertEqual(Path('~/foo/bar/').expanduser(), Path('/root/foo/bar'))

            self.assertNotEqual(os.environ['SUDO_UID'], user_id)
            self.assertNotEqual(os.environ['SUDO_GID'], user_group_id)

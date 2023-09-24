from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from bx_py_utils.test_utils.redirect import RedirectOut

from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles


class SnapshotTestCase(TestCase):
    maxDiff = None

    def test_updatetestsnapshotfiles(self):
        with TemporaryDirectory(prefix='test_updatetestsnapshotfiles_') as temp:
            temp_path = Path(temp)

            snapshot1 = temp_path / 'one.snapshot.ext'
            snapshot1.touch()

            snapshot2 = temp_path / 'foo' / 'two.snapshot.ext'
            snapshot2.parent.mkdir()
            snapshot2.touch()

            with NoColorEnvRich(), RedirectOut() as buffer, UpdateTestSnapshotFiles(
                root_path=temp_path, verbose=True
            ) as cm:
                self.assertFalse(snapshot1.is_file())
                self.assertFalse(snapshot2.is_file())

                self.assertEqual(sorted(cm.get_snapshotfiles()), [])

                snapshot2.touch()

                self.assertEqual(sorted(cm.get_snapshotfiles()), [snapshot2])

            self.assertEqual(buffer.stderr, '')
            self.assertEqual(
                buffer.stdout,
                '2 test snapshot files removed...\n1 test snapshot files created, ok.\n\n',
            )
            self.assertEqual(sorted(cm.get_snapshotfiles()), [snapshot2])

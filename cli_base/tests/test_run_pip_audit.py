from unittest import TestCase
from unittest.mock import patch

from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from cli_base.cli_tools.test_utils.temp_utils import FakeNamedTemporaryFile
from cli_base.constants import PY_BIN_PATH
from cli_base.run_pip_audit import run_pip_audit


class RunPipAuditTestCase(TestCase):
    def test_happy_path(self):
        with (
            SubprocessCallMock(
                return_callback=SimpleRunReturnCallback(stdout=b'mocked output'),  # type: ignore
            ) as call_mock,
            patch('tempfile.NamedTemporaryFile', FakeNamedTemporaryFile),
        ):
            run_pip_audit()
        self.assertEqual(
            call_mock.get_popenargs(rstrip_paths=(PY_BIN_PATH,)),
            [
                [
                    '.../uv',
                    'export',
                    '--no-header',
                    '--frozen',
                    '--no-editable',
                    '--no-emit-project',
                ],
                [
                    '.../pip-audit',
                    '--strict',
                    '--require-hashes',
                    '--disable-pip',
                    '-r',
                    '/tmp/requirements<rnd>.txt',
                ],
            ],
        )

from unittest import TestCase

from bx_py_utils.doc_write.api import GeneratedInfo, generate

from cli_base.cli_dev import PACKAGE_ROOT


class DocuWriteApiTestCase(TestCase):
    def test_up2date_docs(self):
        info: GeneratedInfo = generate(base_path=PACKAGE_ROOT)
        self.assertGreaterEqual(len(info.paths), 1)
        self.assertEqual(info.update_count, 0, 'No files should be updated, commit the changes')
        self.assertEqual(info.remove_count, 0, 'No files should be removed, commit the changes')

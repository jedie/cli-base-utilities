from pathlib import Path
from unittest import TestCase

from cli_base.cli_tools.dict_utils import replace_dict_values_prefix


class DictUtilsTestCase(TestCase):
    def test_replace_dict_values_prefix(self):
        data = {'foo': '123FOO', 'bar': {'baz': Path('123BAR')}}
        replace_dict_values_prefix(data, prefix='123', new_prefix='xxx')
        self.assertEqual(data, {'foo': 'xxxFOO', 'bar': {'baz': Path('xxxBAR')}})

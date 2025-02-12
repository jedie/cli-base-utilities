import dataclasses
import inspect
from unittest import TestCase

import tomlkit
from tomlkit import TOMLDocument

from cli_base.constants import PY313
from cli_base.toml_settings.serialize import dataclass2toml, dataclass2toml_str
from cli_base.toml_settings.tests.fixtures import ComplexExample, PathExample, SimpleExample


class SerializeTestCase(TestCase):
    def test_dataclass2toml_simple(self):
        document = dataclass2toml(instance=SimpleExample())
        self.assertIsInstance(document, TOMLDocument)
        self.assertEqual(document.unwrap(), {'one': 'foo', 'two': 'bar', 'three': '', 'number': 123})

        doc_str = tomlkit.dumps(document, sort_keys=False).rstrip()
        self.assertEqual(
            doc_str,
            inspect.cleandoc(
                '''
                # A simple example
                one = "foo"
                two = "bar"
                three = ""
                number = 123
                '''
            ),
        )

    def test_dataclass2toml_str(self):
        toml_str = dataclass2toml_str(instance=SimpleExample())
        self.assertEqual(
            toml_str,
            inspect.cleandoc(
                '''
                # A simple example
                one = "foo"
                two = "bar"
                three = ""
                number = 123
                '''
            ),
        )

    def test_dataclass2toml_path(self):
        document = dataclass2toml(instance=PathExample())
        self.assertIsInstance(document, TOMLDocument)
        self.assertEqual(document.unwrap(), {'path': '/foo/bar'})

        doc_str = tomlkit.dumps(document, sort_keys=False).rstrip()
        if PY313:
            # FIXME: The "._local." part is just ugly :(
            self.assertEqual(
                doc_str,
                inspect.cleandoc(
                    '''
                    # PathExample(path: pathlib._local.Path = PosixPath('/foo/bar'))
                    path = "/foo/bar"
                    '''
                ),
            )
        else:
            self.assertEqual(
                doc_str,
                inspect.cleandoc(
                    '''
                    # PathExample(path: pathlib.Path = PosixPath('/foo/bar'))
                    path = "/foo/bar"
                    '''
                ),
            )

    def test_dataclass2toml_inheritance(self):
        instance = ComplexExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'foo': 'bar',
                'sub_class_one': {'number': 123},
                'sub_class_two': {'something': 0.5},
                'sub_class_three': {'one_value': True},
            },
        )

        document = dataclass2toml(instance=instance)
        self.assertIsInstance(document, TOMLDocument)
        self.assertEqual(document.unwrap(), data)

        doc_str = tomlkit.dumps(document, sort_keys=False).rstrip()
        self.assertEqual(
            doc_str,
            inspect.cleandoc(
                '''
                # This is the doc string, of the first level.
                # It's two lines of doc string ;)
                foo = "bar"

                [sub_class_one]
                # This is SubClass ONE on second level of FirstLevel
                number = 123

                [sub_class_two]
                # This is SubClass TWO on second level of FirstLevel
                something = 0.5

                [sub_class_three]
                # SubClass3(one_value: bool = True)
                one_value = true
                '''
            ),
        )

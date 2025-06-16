import dataclasses
import inspect
import logging
from pathlib import Path
from unittest import TestCase

import tomlkit

from cli_base.toml_settings.deserialize import toml2dataclass
from cli_base.toml_settings.tests.fixtures import ComplexExample, PathExample, SimpleExample


class DeserializeTestCase(TestCase):
    def test_toml2dataclass_simple(self):
        instance = SimpleExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(data, {'one': 'foo', 'two': 'bar', 'three': '', 'number': 123})

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                # Own Comment,
                # should be keep
                two = "New Value"
                three = 666 # Wrong type!
                number = 123 # Contains the same value!

                [other]
                foo = "bar"
                '''
            ),
        )
        with self.assertLogs(logger=None, level=logging.DEBUG) as logs:
            toml2dataclass(document=document, instance=instance)
        print('\n'.join(logs.output))

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'one': 'foo',
                'two': 'New Value',  # <<< changed
                'three': '',
                'number': 123,
            },
        )
        toml = tomlkit.dumps(document)
        self.assertEqual(
            toml,
            inspect.cleandoc(
                '''
                # Own Comment,
                # should be keep
                two = "New Value"
                three = "" # Wrong type!
                number = 123 # Contains the same value!
                one = "foo"

                [other]
                foo = "bar"
                '''
            ),
        )

        self.assertEqual(
            logs.output,
            [
                "INFO:cli_base.toml_settings.deserialize:Missing 'one' in toml config",
                #
                "INFO:cli_base.toml_settings.deserialize:Take over 'two' from user toml setting",
                #
                'ERROR:cli_base.toml_settings.deserialize:Toml value three=666 is type '
                "'int' but must be type 'str' -> ignored and use default value!",
                #
                'DEBUG:cli_base.toml_settings.deserialize:Default value 123 also used in toml file, ok.',
            ],
        )

    def test_toml2dataclass_path(self):
        instance = PathExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'path': Path('/foo/bar'),
            },
        )

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                path = "/to/some/other/place/"
                '''
            ),
        )

        toml2dataclass(document=document, instance=instance)

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'path': Path('/to/some/other/place'),
            },
        )

    def test_toml2dataclass_inheritance(self):
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

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                [sub_class_one]
                number = "Not a Number!"

                [sub_class_two]
                something = 123.456
                '''
            ),
        )
        with self.assertLogs(logger=None, level=logging.DEBUG) as logs:
            toml2dataclass(document=document, instance=instance)
        print('\n'.join(logs.output))

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'foo': 'bar',  # <<< not change, because not in toml file
                'sub_class_one': {
                    'number': 123,  # <<< not change, because wrong type
                },
                'sub_class_two': {
                    'something': 123.456,  # <<< updated
                },
                'sub_class_three': {'one_value': True},  # <<< added
            },
        )
        toml = tomlkit.dumps(document).rstrip()
        self.assertEqual(
            toml,
            inspect.cleandoc(
                '''
                foo = "bar"

                [sub_class_one]
                number = 123

                [sub_class_two]
                something = 123.456
                [sub_class_three]
                # SubClass3(one_value: bool = True)
                one_value = true
                '''
            ),
        )

        self.assertEqual(
            logs.output,
            [
                "INFO:cli_base.toml_settings.deserialize:Missing 'foo' in toml config",
                #
                "ERROR:cli_base.toml_settings.deserialize:Toml value number='Not a "
                "Number!' is type 'str' but must be type 'int' -> ignored and use default "
                'value!',
                #
                "INFO:cli_base.toml_settings.deserialize:Take over 'something' from user toml setting",
                #
                'INFO:cli_base.toml_settings.deserialize:Missing complete sub dataclass '
                "'sub_class_three' in toml config",
            ],
        )

    def test_toml2dataclass_boolean_flag(self):
        @dataclasses.dataclass
        class BooleanExample:
            flag: bool = False

        instance = BooleanExample()
        self.assertIs(instance.flag, False)

        document = tomlkit.loads('flag = true')
        changed = toml2dataclass(document=document, instance=instance)
        self.assertIs(changed, False)  # both are boolean values
        self.assertIs(instance.flag, True)  # takeover the value from toml file

        # Test again with non boolean value:

        instance = BooleanExample()
        self.assertIs(instance.flag, False)

        document = tomlkit.loads('flag = "no boolean"')
        with self.assertLogs(logger=None, level=logging.DEBUG) as logs:
            changed = toml2dataclass(document=document, instance=instance)
        self.assertIs(changed, True)  # String convert to boolean
        self.assertIs(instance.flag, False)  # The default
        self.assertEqual(
            logs.output,
            [
                "ERROR:cli_base.toml_settings.deserialize:"
                "Toml value flag='no boolean' is not a boolean"
                " -> ignored and use default value: False"
            ],
        )

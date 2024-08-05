from __future__ import annotations

import dataclasses
import logging
from pathlib import Path

import tomlkit
from tomlkit import TOMLDocument
from tomlkit.items import Table

from cli_base.toml_settings.data_class_utils import iter_dataclass
from cli_base.toml_settings.serialize import add_dataclass


logger = logging.getLogger(__name__)


def toml2dataclass(*, document: TOMLDocument | Table, instance, _changed=False) -> bool:
    """
    Sync toml and instance in place:

     - Transfer all valid values from toml document into the data class instance
     - Add missing or invalid values to the toml document
    """

    for field_name, field_value in iter_dataclass(instance):
        if dataclasses.is_dataclass(field_value):
            try:
                sub_doc = document[field_name]
            except KeyError:
                logger.info('Missing complete sub dataclass %r in toml config', field_name)
                document.add(tomlkit.nl())  # Add new line
                add_dataclass(document=document, name=field_name, instance=field_value)
                _changed = True
            else:
                changed = toml2dataclass(document=sub_doc, instance=field_value, _changed=_changed)
                if changed:
                    _changed = True
            continue

        try:
            doc_value = document[field_name]
        except KeyError:
            logger.info('Missing %r in toml config', field_name)

            # Add missing item, so that the toml file can be updated on disk:
            document[field_name] = field_value
            _changed = True
            continue

        if field_value == doc_value:
            logger.debug('Default value %r also used in toml file, ok.', field_value)
        elif isinstance(field_value, Path):
            logger.debug('Convert %r value %r to Path instance', field_name, field_value)
            value = doc_value.unwrap()
            if not isinstance(value, str):
                logger.error(
                    (
                        'Toml value %s=%r is type %r but must be type str (Will be convert to Path instance)'
                        ' -> ignored and use default value!'
                    ),
                    field_name,
                    value,
                    type(value).__name__,
                )
                document[field_name] = field_value  # Add default one
                _changed = True
            else:
                setattr(instance, field_name, Path(value))
        elif isinstance(field_value, bool):
            if not isinstance(doc_value, bool):
                logger.error(
                    'Toml value %s=%r is not a boolean -> ignored and use default value: %r',
                    field_name,
                    doc_value,
                    field_value,
                )
                setattr(instance, field_name, field_value)
                _changed = True
            else:
                logger.info('Take over %r for %r from user toml setting', doc_value, field_name)
                setattr(instance, field_name, doc_value)
        elif not isinstance(field_value, type(doc_value.unwrap())):
            logger.error(
                'Toml value %s=%r is type %r but must be type %r -> ignored and use default value!',
                field_name,
                doc_value,
                type(doc_value.unwrap()).__name__,
                type(field_value).__name__,
            )
            document[field_name] = field_value  # Add default one
            _changed = True
        else:
            logger.info('Take over %r from user toml setting', field_name)
            setattr(instance, field_name, doc_value)

    return _changed

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path

import tomlkit
from tomlkit import TOMLDocument
from tomlkit.items import Table

from cli_base.toml_settings.data_class_utils import iter_dataclass


def add_docstring(document: TOMLDocument | Table, instance):
    if doc_string := inspect.getdoc(instance):
        for line in doc_string.strip().splitlines():
            document.add(tomlkit.comment(line))


def add_value(*, field_name, item: TOMLDocument | Table, value):
    if isinstance(value, Path):
        value = str(value)

    item.add(field_name, value)


def add_dataclass(document: TOMLDocument | Table, name, instance):
    assert dataclasses.is_dataclass(instance), f'No dataclass: {instance!r}'

    table = tomlkit.table()
    add_docstring(table, instance)

    for field_name, field_value in iter_dataclass(instance):
        if dataclasses.is_dataclass(field_value):
            add_dataclass(table, field_name, field_value)
        else:
            add_value(field_name=field_name, item=table, value=field_value)

    document.add(name, table)


def dataclass2toml(instance) -> TOMLDocument:
    """
    Serialize a dataclass to a tomlkit document.
    """
    assert dataclasses.is_dataclass(instance), f'No dataclass: {instance!r}'

    document = tomlkit.document()
    add_docstring(document, instance)

    for field_name, field_value in iter_dataclass(instance):
        if dataclasses.is_dataclass(field_value):
            add_dataclass(document, field_name, field_value)
        else:
            add_value(field_name=field_name, item=document, value=field_value)

    return document


def dataclass2toml_str(instance) -> str:
    """
    Serialize a dataclass to a toml string.
    """
    document: TOMLDocument = dataclass2toml(instance=instance)
    doc_str = tomlkit.dumps(document, sort_keys=False)
    return doc_str.strip()

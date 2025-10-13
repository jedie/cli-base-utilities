import dataclasses
import inspect
import textwrap
from collections.abc import Iterable

from bx_py_utils.anonymize import anonymize
from rich import print  # noqa
from rich.console import Console
from rich.style import Style

from cli_base.toml_settings.data_class_utils import iter_dataclass


DEFAULT_STYLE = Style(bgcolor='#090909')


def print_dataclasses(*, instance, anonymize_keys: Iterable, indent=0, style=DEFAULT_STYLE, console=None) -> set[str]:
    console = console or Console()

    console.print(f'{" " * indent}[magenta]{instance.__class__.__name__}[/magenta]:', style=style)

    indent += 2

    if doc_string := inspect.getdoc(instance):
        console.print(textwrap.indent(doc_string, prefix=' ' * indent), style=style)

    indent += 2

    anonymized = set()

    for field_name, field_value in iter_dataclass(instance):
        if dataclasses.is_dataclass(field_value):
            console.print()
            anonymized |= print_dataclasses(
                instance=field_value, anonymize_keys=anonymize_keys, indent=indent + 4, style=style, console=console
            )
        else:
            if field_name in anonymize_keys:
                field_value = anonymize(field_value)
                anonymized.add(field_name)
            console.print(f'{" " * indent}* [cyan]{field_name}[/cyan] = {field_value!r}', style=style)
    return anonymized

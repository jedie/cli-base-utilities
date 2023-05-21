from pathlib import Path


def replace_prefix(text: str, *, prefix: str, new_prefix: str) -> str:
    """
    >>> replace_prefix('foobar', prefix='foo', new_prefix='FOO')
    'FOObar'
    >>> replace_prefix('foobar', prefix='no', new_prefix='yes')
    'foobar'
    """
    if text.startswith(prefix):
        return f'{new_prefix}{text.removeprefix(prefix)}'
    return text


def replace_dict_values_prefix(data: dict, *, prefix: str, new_prefix: str) -> None:
    """
    Replace prefixes in dict values, recusive and in-place. Works with Path() values, too.

    Usecase: You have a dict structure with many temp file path
    and would like to replace all random temp path prefixes ;)

    >>> data = {'foo': '123FOO', 'bar': {'baz': '123BAR'}}
    >>> replace_dict_values_prefix(data, prefix='123', new_prefix='xxx')
    >>> data
    {'foo': 'xxxFOO', 'bar': {'baz': 'xxxBAR'}}
    """
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(prefix):
            data[key] = replace_prefix(value, prefix=prefix, new_prefix=new_prefix)
        elif isinstance(value, Path) and str(value).startswith(prefix):
            data[key] = Path(replace_prefix(str(value), prefix=prefix, new_prefix=new_prefix))
        elif isinstance(value, dict):
            replace_dict_values_prefix(value, prefix=prefix, new_prefix=new_prefix)

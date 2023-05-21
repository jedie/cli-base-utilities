import dataclasses
from string import Template


class InvalidTemplate(AssertionError):
    pass


class InvalidTemplateKeys(InvalidTemplate):
    pass


@dataclasses.dataclass
class TemplateKeyInfo:
    template_keys: list[str]
    not_in_context: list[str]  # Keys are in template, but not in context
    not_in_template: list[str]  # Keys are in context, but not in template
    invalid_keys: list[str]


def get_template_key_info(*, content: str, context: dict) -> TemplateKeyInfo:
    template = Template(content)
    template_keys = set()
    invalid_keys = set()
    for mo in template.pattern.finditer(content):
        if name := (mo.group('named') or mo.group('braced')):
            template_keys.add(name)
        elif invalid := mo.group('invalid'):
            invalid_keys.add(invalid)

    context_keys = set(context.keys())
    return TemplateKeyInfo(
        template_keys=sorted(template_keys),
        not_in_template=sorted(context_keys - template_keys),
        not_in_context=sorted(template_keys - context_keys),
        invalid_keys=sorted(invalid_keys),
    )


def repr_keys(keys):
    """
    >>> repr_keys(['Foo', True, 1])
    '"Foo", "True", "1"'
    """
    return ', '.join(f'"{key}"' for key in keys)


def validate_template(*, content: str, context: dict) -> None:
    info: TemplateKeyInfo = get_template_key_info(content=content, context=context)

    errors = []
    if keys := info.not_in_context:
        errors.append(f'Template key(s) {repr_keys(keys)} not in context')

    if keys := info.not_in_template:
        errors.append(f'Context key(s) {repr_keys(keys)} not in template')

    if keys := info.invalid_keys:
        errors.append(f'Template key(s) {repr_keys(keys)} invalid')

    if errors:
        raise InvalidTemplate(' & '.join(errors))

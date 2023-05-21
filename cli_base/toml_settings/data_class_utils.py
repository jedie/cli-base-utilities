import dataclasses


def iter_dataclass(instance):
    for field in dataclasses.fields(instance):
        field_name = field.name
        field_value = getattr(instance, field_name)
        yield field_name, field_value

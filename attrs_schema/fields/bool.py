import attr
from attr.validators import instance_of
from ..compat import string_type


def to_bool(value):
    if isinstance(value, string_type):
        return value.lower().startswith("t")
    return bool(value)

Bool = attr.ib(
    validator=instance_of(bool),
    convert=to_bool,
    metadata={"jsonschema": {"type": "boolean"}}
)

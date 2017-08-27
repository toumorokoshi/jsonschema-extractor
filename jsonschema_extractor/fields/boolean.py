import attr
from attr.validators import instance_of
from ..compat import string_type
from ..utils import merge_attributes


def to_bool(value):
    if isinstance(value, string_type):
        return value.lower().startswith("t")
    return bool(value)


def boolean(**kwargs):
    kwargs = merge_attributes({
        "validator": instance_of(bool),
        "convert": to_bool,
        "metadata": {
            "jsonschema": {
                "type": "boolean"
            }
        }
    }, kwargs)
    return attr.ib(**kwargs)

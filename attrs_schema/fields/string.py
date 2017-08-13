import attr
from attr.validators import instance_of
from ..compat import string_type
from ..utils import merge_attributes


def to_string(value):
    if isinstance(value, string_type):
        return value
    return str(value)


def string(**kwargs):
    kwargs = merge_attributes({
        "validator": instance_of(string_type),
        "convert": to_string,
        "metadata": {
            "jsonschema": {
                "type": "string"
            }
        }
    }, kwargs)
    return attr.ib(**kwargs)

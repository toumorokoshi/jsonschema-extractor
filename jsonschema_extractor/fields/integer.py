import attr
from attr.validators import instance_of
from ..utils import merge_attributes


def to_integer(value):
    return int(value)


def integer(**kwargs):
    kwargs = merge_attributes({
        "validator": instance_of(int),
        "convert": to_integer,
        "metadata": {
            "jsonschema": {
                "type": "integer"
            }
        }
    }, kwargs)
    return attr.ib(**kwargs)

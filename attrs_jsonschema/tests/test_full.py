import attr
import pytest
from attr.validators import instance_of
from attrs_jsonschema import extract, UnextractableSchema


@attr.s
class Example(object):
    an_int = attr.ib(validator=instance_of(int))
    a_bool = attr.ib(validator=instance_of(bool))
    a_string = attr.ib(validator=[
        instance_of(str)
    ], default="foo")

SCHEMA_PAIRS = [
    (Example, {
        "title": "Example",
        "type": "object",
        "properties": {
            "an_int": {"type": "integer"},
            "a_string": {"type": "string"},
            "a_bool": {"type": "boolean"},
        },
        "required": ["an_int", "a_bool"]
    })
]


@pytest.mark.parametrize("obj,expected_schema",
                         SCHEMA_PAIRS)
def test_extract_schema(obj, expected_schema):
    assert extract(obj) == expected_schema


def test_non_attrs_object():
    """
    non-attrs objects should raise an exception
    when attempted to be extracted.
    """
    class Foo(object):
        def __init__(self, x):
            self.x = x

    with pytest.raises(UnextractableSchema):
        extract(Foo)


def test_attribute_missing_validation():
    """
    non-attrs objects should raise an exception
    when attempted to be extracted.
    """

    @attr.s
    class Foo(object):
        something = attr.ib()

    with pytest.raises(UnextractableSchema):
        extract(Foo)

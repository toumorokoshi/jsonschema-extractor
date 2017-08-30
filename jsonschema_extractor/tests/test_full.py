import attr
import pytest
from attr.validators import instance_of
from jsonschema_extractor import extract_jsonschema, extract


@attr.s
class Example(object):
    an_int = attr.ib(validator=instance_of(int))
    a_bool = attr.ib(validator=instance_of(bool))
    a_string = attr.ib(validator=instance_of(str), default="foo")

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
    assert extract_jsonschema(obj) == expected_schema


def test_extractor_regular_class(extractor):
    class Foo(object):
        pass

    extract(Foo) == {"type": "object"}

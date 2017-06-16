import attr
import pytest
from attr.validators import instance_of
from attrs_jsonschema import extract_schema


@attr.s
class Test(object):
    an_int = attr.ib(validators=instance_of(int))

SCHEMA_PAIRS = [
    (Test, {
        "title": "Test",
        "type": "object",
        "properties": {
            "an_int": {"type": "integer"}
        }
    })
]


@pytest.mark.parametrize("obj,expected_schema",
                         SCHEMA_PAIRS)
def test_extract_schema(obj, expected_schema):
    assert extract_schema(obj) == expected_schema

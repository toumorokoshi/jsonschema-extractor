import attr
import pytest
from attr.validators import instance_of
from jsonschema_extractor import UnextractableSchema


@attr.s
class Example(object):
    integer = attr.ib(validator=instance_of(int))
    foo = attr.ib(metadata={"jsonschema": {
        "type": "string", "format": "uuid"
    }})
    validator_list = attr.ib(validator=[
        instance_of(float)
    ])
    string = attr.ib(validator=instance_of(str), default="foo")

def test_extract_attrs(extractor):
    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "validator_list": {"type": "number"},
            "foo": {"type": "string", "format": "uuid"}
        },
        "required": ["integer", "foo", "validator_list"]
    }


def test_unextractable_schema(extractor):
    """ test an attrs class which we can't extract schema from. """
    @attr.s
    class NoBueno(object):
        foo = attr.ib()
    with pytest.raises(UnextractableSchema):
        extractor.extract(NoBueno)

from typing import List

import attr
import pytest
from attr.validators import instance_of

from jsonschema_extractor import UnextractableSchema


@attr.define
class Example(object):
    integer: int = attr.field()
    foo = attr.field(metadata={"jsonschema": {"type": "string", "format": "uuid"}})
    validator_list: List[float] = attr.field()
    floating_point: float = attr.field(validator=instance_of(float))
    string: str = attr.field(
        default="foo", metadata={"description": "This is an description."}
    )


def test_extract_attrs(extractor):
    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "floating_point": {"type": "number"},
            "string": {"description": "This is an description.", "type": "string"},
            "integer": {"type": "integer"},
            "validator_list": {"items": {"type": "number"}, "type": "array"},
            "foo": {"type": "string", "format": "uuid"},
        },
        "required": ["integer", "foo", "validator_list", "floating_point"],
    }


def test_unextractable_schema(extractor):
    """test an attrs class which we can't extract schema from."""

    @attr.s
    class NoBueno(object):
        foo = attr.ib()

    with pytest.raises(UnextractableSchema):
        extractor.extract(NoBueno)

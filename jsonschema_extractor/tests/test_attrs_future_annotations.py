from __future__ import annotations

# similar to test_attrs, but specifically testing
# future imports.
from typing import List

import attr
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

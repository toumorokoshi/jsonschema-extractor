import attr
from typing import Optional


@attr.s
class Example(object):
    integer = attr.ib(type=int)
    optional = attr.ib(type=Optional[str])
    string = attr.ib(type=str, default="foo")


def test_extract_cattrs(extractor):
    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "optional": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
        "required": ["integer", "optional"],
    }

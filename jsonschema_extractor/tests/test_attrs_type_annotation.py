import attr
from typing import Optional

from jsonschema_extractor.typing_extractor import PY_36

@attr.s
class Example(object):
    integer = attr.ib(type=int)
    string = attr.ib(type=str, default="foo")


@attr.s
class ExampleOptional(object):
    optional = attr.ib(type=Optional[str])


def test_extract_cattrs(extractor):
    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "string": {"type": "string"},
            "integer": {"type": "integer"}
        },
        "required": ["integer"]
    }


def test_extract_cattrs_optional(extractor):
    if not PY_36:
        return
    assert extractor.extract(ExampleOptional) == {
        "type": "object",
        "title": "ExampleOptional",
        "properties": {
            "optional": {"type": "string", "nullable": True}
        },
        "required": ["optional"]
    }

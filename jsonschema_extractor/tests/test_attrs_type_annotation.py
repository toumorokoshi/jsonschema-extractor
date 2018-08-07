import attr
import sys
from typing import Optional

PY_36 = sys.version_info[:2] >= (3, 6)

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
            "integer": {"type": "integer"},
            # "optional": {"type": "integer", "nullable": True}
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

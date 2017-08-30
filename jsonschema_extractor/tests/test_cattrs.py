import attr
from cattr import typed


@attr.s
class Example(object):
    integer = typed(int)
    string = typed(str, default="foo")

def test_extract_cattrs(extractor):
    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
        },
        "required": ["integer"]
    }

import attr

@attr.s
class Example(object):
    integer = attr.ib(type=int)
    string = attr.ib(type=str, default="foo")

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

import pytest
from attrs_schema import boolean


def test_bool_metadata():
    boolean().metadata["jsonschema"] == {
        "type": "boolean"
    }


@pytest.mark.parametrize("inp, result", [
    ("true", True),
    ("false", False),
    (1, True),
    (0, False),
    (True, True),
    (False, False),
    (object(), True),
])
def test_bool_validation(inp, result):
    b = boolean()
    assert b.convert(inp) is result

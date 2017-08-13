import pytest
from attrs_schema.fields import Bool


def test_bool_metadata():
    assert Bool.metadata["jsonschema"] == {
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
    assert Bool.convert(inp) is result

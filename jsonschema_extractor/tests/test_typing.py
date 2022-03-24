import pytest
import sys
from datetime import datetime
from typing import Any, List, Set, Optional, Union
from jsonschema_extractor.typing_extractor import TypingExtractor
from jsonschema_extractor.typing_extractor import _is_union

PEP_560 = sys.version_info[:3] >= (3, 7, 0)


@pytest.fixture
def typing_extractor():
    return TypingExtractor()


@pytest.mark.parametrize(
    "inp, expected_output",
    [
        (int, {"type": "integer"}),
        (float, {"type": "number"}),
        (str, {"type": "string"}),
        (type(None), {"type": "null"}),
        (datetime, {"type": "string", "format": "date-time"}),
        (
            Optional[int],
            {
                "anyOf": [
                    {"type": "integer"},
                    {"type": "null"},
                ]
            },
        ),
        (
            Union[int, str],
            {
                "anyOf": [
                    {"type": "integer"},
                    {"type": "string"},
                ]
            },
        ),
        (List[int], {"type": "array", "items": {"type": "integer"}}),
    ],
)
def test_extract_typing(extractor, inp, expected_output):
    assert extractor.extract(inp) == expected_output


@pytest.mark.skipif(PEP_560, reason="sets are not PEP_560 compatible")
def test_typing_extractor_register(typing_extractor):
    def extract_set(extractor, typ):
        subtype = Any
        if typ.__args__ and typ.__args__[0] is not Any:
            subtype = typ.__args__[0]
        return {
            "type": "array",
            "title": "set",
            "items": extractor.extract(extractor, subtype),
        }

    typing_extractor.register(set, extract_set)

    assert typing_extractor.extract(typing_extractor, Set[int]) == {
        "type": "array",
        "title": "set",
        "items": {"type": "integer"},
    }


def test_typing_extractor_register(typing_extractor):
    class Foo(object):
        pass

    def extract_foo(extractor, typ):
        return {
            "type": "string",
        }

    typing_extractor.register(Foo, extract_foo)

    assert typing_extractor.extract(typing_extractor, Foo) == {
        "type": "string",
    }


def test_is_union():
    assert _is_union(Optional[int])


def test_typing_extractor_nontype(extractor):
    """The typing extractor shouldn't fail with a non-type passed in.

    Users may want to have a custom type annotation.
    """
    assert extractor.extract(object()) == {"type": "object"}


def test_typing_extractor_int_enum(typing_extractor):
    """A custom extractor for an IntEnum should match.

    This tests case catches an issue where an IntEnum was
    matched with the integer extractor, despite a custom type
    being matched to it. (GitHub #9)
    """
    from enum import IntEnum

    class Test(IntEnum):
        A = 1
        B = 2
        C = 3

    typing_extractor.register(
        IntEnum, lambda extractor, typ: {"enum": [c.name for c in typ]}
    )
    assert typing_extractor.extract(None, Test) == {"enum": ["A", "B", "C"]}

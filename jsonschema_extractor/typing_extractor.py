import sys
from datetime import datetime
from .compat import string_type
from typing import Any, List, Sequence, Union


class TypingExtractor(object):
    def __init__(self):
        # extractor_list is a function-based
        # extractor type, designed to handle
        # non-discrete types like Unions or
        # sequences.
        self._extractor_list = [
            (_is_union, _extract_union),
            (_is_sequence, _extract_seq),
        ]
        # extractor by type exists to handle specific
        # types. A dict is used as a list-based approach
        # may choose a match that is higher in the list, but
        # incorrect as there is a more specific type that could
        # be matched.
        self._extractor_by_type = {
            bool: _extract_bool,
            datetime: _extract_datetime,
            list: _extract_seq,
            int: _extract_int,
            float: _extract_float,
            string_type: _extract_string,
            type(None): _extract_null,
        }

    @staticmethod
    def can_handle(typ):
        return True

    def extract(self, extractor, typ):
        if isinstance(typ, type):
            for subtype in typ.__mro__:
                handler = self._extractor_by_type.get(subtype)
                if handler is not None:
                    return handler(extractor, typ)
        else:
            for is_type, handler in self._extractor_list:
                if is_type(typ):
                    return handler(extractor, typ)
        return _extract_fallback(extractor, typ)

    def register(self, typ, handler):
        """
        if you need to add additional types, you
        can do so with this API.
        """
        if isinstance(type(typ), type):
            self._extractor_by_type[typ] = handler
        else:
            self._extractor_list.append((typ, handler))


def _extract_fallback(extractor, typ):
    return {"type": "object"}


def _extract_union(extractor, union):
    return {"anyOf": [extractor.extract(t) for t in union.__args__]}


def _extract_seq(extractor, seq):
    """Convert a sequence to primitive equivalents."""
    subtype = Any
    if seq.__args__ and seq.__args__[0] is not Any:
        subtype = seq.__args__[0]
    return _array_type(extractor.extract(subtype))


def _array_type(subtype_schema):
    return {"type": "array", "items": subtype_schema}


def _extract_int(extractor, typ):
    return {"type": "integer"}


def _extract_float(extractor, typ):
    return {"type": "number"}


def _extract_string(extractor, typ):
    return {"type": "string"}


def _extract_bool(extractor, typ):
    return {"type": "boolean"}


def _extract_null(extractor, typ):
    return {"type": "null"}


def _extract_datetime(extractor, typ):
    return {"type": "string", "format": "date-time"}


def _is_sequence(typ):
    """
    returns True if the type in question
    is a Sequence[] object from the typing module.
    """
    # PEP_560 deprecates issubclass for
    # List types, for the time being
    # we'll support a specific escape hatch.
    if hasattr(typ, "__origin__"):
        return issubclass(typ.__origin__, Sequence)
    return False


def _is_union(typ):
    if hasattr(typ, "__origin__"):
        return typ.__origin__ is Union
    return False

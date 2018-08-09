import sys
from datetime import datetime
from .compat import string_type
from typing import (
    Any, List, Sequence
)
PEP_560 = sys.version_info[:3] >= (3, 7, 0)
if PEP_560:  # pragma: no cover
    from typing import _GenericAlias
    # from typing import _SpecialForm
else:
    from typing import _Union

class TypingExtractor(object):

    def __init__(self):
        self._extractor_list = []
        self._extractor_list.append((string_type, _extract_string))
        if PEP_560:  # pragma: no cover
            self._extractor_list.append((List, _extract_seq))
        self._extractor_list.append((Sequence, _extract_seq))
        self._extractor_list.append((bool, _extract_bool))
        self._extractor_list.append((int, _extract_int))
        self._extractor_list.append((float, _extract_float))
        self._extractor_list.append((datetime, _extract_datetime))
        self._extractor_list.append((type(None), _extract_null))

    @staticmethod
    def can_handle(typ):
        return True

    def extract(self, extractor, typ):
        # PEP_560 deprecates issubclass for
        # List types, for the time being
        # we'll support a specific escape hatch.
        if PEP_560:  # pragma: no cover
            if isinstance(typ, _GenericAlias) and typ.__origin__ is list:
                return _extract_seq(extractor, typ)
            # TODO: test on PY_37
            # if isinstance(typ, _SpecialForm) and typ._name == 'Optional':
                # return _extract_optional(extractor, typ, self._extractor_list)
        if isinstance(typ, _Union):
            assert len(typ.__args__) == 2 # Optional can only have one type and None
            return _extract_optional(extractor, typ, self._extractor_list)
        for t, t_extractor in self._extractor_list:
            if issubclass(typ, t):
                return t_extractor(extractor, typ)
        return _extract_fallback(extractor, typ)

    def register(self, typ, handler):
        """
        if you need to add additional types, you
        can do so with this API.
        """
        self._extractor_list.append((typ, handler))


def _extract_fallback(extractor, typ):
    return {"type": "object"}


def _extract_optional(extractor, optional, extractor_list):
    nullable_typ = optional.__args__[0]
    type_schema = _extract_fallback(extractor, optional)
    for t, t_extractor in extractor_list:
        if issubclass(nullable_typ, t):
            type_schema = t_extractor(extractor, optional)
            break
    type_schema["nullable"] = True
    return type_schema


def _extract_seq(extractor, seq):
    """Convert a sequence to primitive equivalents."""
    subtype = Any
    if seq.__args__ and seq.__args__[0] is not Any:
        subtype = seq.__args__[0]
    return _array_type(extractor.extract(subtype))


def _array_type(subtype_schema):
    return {
        "type": "array",
        "items": subtype_schema
    }


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

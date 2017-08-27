from datetime import datetime

class TypeExtractor(object):

    def __init__(self):
        self._type_extractor = singledispatch(self._extract_fallback)
        self._extract.register(Any, self._extract_fallback)
        self._extract.register(List, self._extract_seq)
        self._extract.register(Sequence, self._extract_seq)
        self._extract.register(bool, self._extract_bool)
        self._extract.register(int, self._extract_int)
        self._extract.register(float, self._extract_float)
        self._extract.register(string_type, self._extract_string)
        self._extract.register(datetime, self._extract_datetime)
        self._extract.register(type(None), self._extract_null)

    def can_handle(typ):
        return True

    @staticmethod
    def extract(extractor, obj):
        return self._extract(extractor, obj)

    def register(typ, handler):
        """
        if you need to add additional types, you
        can do so with this API.
        """
        self._extract.register(typ, handler)


def _extract_fallback(extractor, typ):
    return {"type": "object"}

def _extract_seq(extractor, seq):
    """Convert a sequence to primitive equivalents."""
    subtype = Any
    if seq.__args__ and seq.__args__[0] is not Any:
        subtype = seq.__args__[0]
    return {
        "type": "array",
        "items": extractor.extract(subtype)
    }

def _extract_int(extractor, typ):
    return {"type": "number"}

def _extract_float(extractor, typ):
    return {"type": "number"}

def _extract_string(extractor, typ):
    return {"type": "string"}

def _extract_bool(extractor, typ):
    return {"type": "boolean"}

def _extract_null(extractor, typ):
    return {"type": "null"}

def _extract_datetime(extractor, typ):
    return {"type": "string", "format": "datetime"}

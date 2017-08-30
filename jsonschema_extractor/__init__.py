from .extractor_set import SchemaExtractorSet

from .typing_extractor import TypingExtractor
DEFAULT_EXTRACTOR_LIST = [
    TypingExtractor()
]
try:
    from .attrs_extractor import AttrsExtractor
    DEFAULT_EXTRACTOR_LIST.insert(0, AttrsExtractor())
except ImportError: # pragma: no cover
    pass # pragma: no cover

def extract_jsonschema(typ):
    return DEFAULT_EXTRACTOR.extract(typ)

def init_default_extractor():
    """
    create a new extractor, providing the default (all available
    extractors)
    """
    return SchemaExtractorSet(DEFAULT_EXTRACTOR_LIST)

DEFAULT_EXTRACTOR = init_default_extractor()
from .exceptions import UnextractableSchema

def extract(cls):
    return DEFAULT_EXTRACTOR.extract(cls)

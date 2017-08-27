from .extractor_set import SchemaExtractorSet
from .attrs_extractor import AttrsExtractor
from .typing_extractor import TypingExtractor

DEFAULT_EXTRACTOR = SchemaExtractorSet([
    AttrsExtractor(),
    TypingExtractor()
])


def extract_jsonschema(typ):
    return DEFAULT_EXTRACTOR.extract(typ)

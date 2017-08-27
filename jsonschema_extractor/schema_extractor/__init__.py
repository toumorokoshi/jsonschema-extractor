from .extractor_set import SchemaExtractorSet
from .attrs_extractor import AttrsExtractor
from .type_extractor import TypeExtractor

DEFAULT_EXTRACTOR = SchemaExtractorSet([
    AttrsExtractor(),
    TypeExtractor()
])

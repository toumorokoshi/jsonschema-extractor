from .set import SchemaExtractorSet

DEFAULT_EXTRACTOR = SchemaExtractorSet([
    AttrsExtractor(),
    TypeExtractor()
])

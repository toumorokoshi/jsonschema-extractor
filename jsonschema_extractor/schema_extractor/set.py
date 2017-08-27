class SchemaExtractorSet(object):
    """
    The SchemaExtractorSet enables joining multiple extractors together,
    choosing the right one based on which one the extractor says it can handle.

    the extractor_list order is important, as the first extractor that states
    it can handle extracting a schema will be used.
    """

    def __init__(self, extractor_list):
        self._extractor_list = extractor_list

    def __getitem__(self, typ):
        """ returns the proper extractor for the typ passed. """
        for extractor in self._extractor_list:
            if extractor.can_handle(typ):
                return extractor

    def extract(self, typ):
        """ extract a schema from an object """
        return self[typ].extract(self, typ)

import attr
from attr.exceptions import (
    NotAnAttrsClassError
)

class AttrsExtractor(object):

    @staticmethod
    def can_handle(typ):
        try:
            attr.fields(typ)
            return True
        except NotAnAttrsClassError:
            return False

    @classmethod
    def extract(cls, extractor, obj):
        """
        take an attrs based class, and convert it
        to jsonschema.
        """
        schema = {
            "title": attrs_class.__name__,
            "type": "object",
            "properties": {},
            "required": []
        }
        for attribute in attr.fields(attrs_class):
            details = extract_attribute(attribute)
            if details.is_required:
                schema["required"].append(details.name)
            schema["properties"][details.name] = details.schema
        return schema

    @classmethod
    def _extract_attribute(cls, extractor, attribute):
        is_required = attribute.default is attr.NOTHING

        schema = None
        if "jsonschema" in attribute.metadata:
            schema = attribute.metadata["jsonschema"]
        else:
            for validator in _iterate_validator(attribute.validator):
                if isinstance(validator, _InstanceOfValidator):
                    schema = extractor.extract(validator.type)

        if schema is None:
            raise UnextractableSchema(
                "all attributes must have an 'InstanceOfValidator'. attribute {0} does not.".format(attribute)
            )
        return AttributeDetails(
            attribute.name, schema, is_required
        )

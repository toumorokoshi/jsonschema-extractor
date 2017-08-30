import attr
from attr.exceptions import (
    NotAnAttrsClassError
)
from .exceptions import UnextractableSchema
from attr.validators import (
    _InstanceOfValidator, _OptionalValidator,
    _AndValidator
)

# copied from cattrs, to enable compatibility with
# the typed parameter from 0.5.0
CATTRS_TYPE_METADATA_KEY = "cattr_type_metadata"

class AttrsExtractor(object):

    @staticmethod
    def can_handle(typ):
        return getattr(typ, "__attrs_attrs__", None) is not None

    @classmethod
    def extract(cls, extractor, typ):
        """
        take an attrs based class, and convert it
        to jsonschema.
        """
        schema = {
            "title": typ.__name__,
            "type": "object",
            "properties": {},
            "required": []
        }
        for attribute in attr.fields(typ):
            details = cls._extract_attribute(extractor, attribute)
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
        elif CATTRS_TYPE_METADATA_KEY in attribute.metadata:
            schema = extractor.extract(attribute.metadata[CATTRS_TYPE_METADATA_KEY])
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

@attr.s
class AttributeDetails(object):
    name = attr.ib()
    schema = attr.ib()
    is_required = attr.ib()

def _iterate_validator(validator):
    if isinstance(validator, _AndValidator):
        for sub_validator in validator._validators:
            yield sub_validator
    else:
        yield validator

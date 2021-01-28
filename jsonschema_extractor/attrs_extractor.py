from enum import Enum, EnumMeta

import attr
from attr.validators import _InstanceOfValidator, _AndValidator, _InValidator

from .exceptions import UnextractableSchema


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
            "required": [],
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

        if "jsonschema" in attribute.metadata:
            schema = attribute.metadata["jsonschema"]
        else:
            schema = cls._extract_attribute_schema_by_type(extractor, attribute)

        if not schema:
            raise UnextractableSchema(
                "all attributes must have an 'InstanceOfValidator' or 'InValidator'. attribute {0} does not.".format(
                    attribute
                )
            )
        return AttributeDetails(attribute.name, schema, is_required)

    @classmethod
    def _extract_attribute_schema_by_type(cls, extractor, attribute):
        """
        Extract the basic schema for the attribute based on its type.
        The type can be supplied to two ways:
        1. The type keyword of attr.ib
        2. The _InstanceValidator of attr
        """
        schema = None
        enum_values = None
        if attribute.type is not None:
            schema = extractor.extract(attribute.type)

        for validator in _iterate_validator(attribute.validator):
            if schema is None and isinstance(validator, _InstanceOfValidator):
                schema = extractor.extract(validator.type)
            if isinstance(validator, _InValidator):
                if isinstance(validator.options, (EnumMeta, Enum)):
                    options = _enum_to_values(validator.options)
                else:
                    options = validator.options

                # Sorting the list for consistency
                enum_values = sorted(list(options))

        if enum_values is not None:
            schema = schema or {}
            schema["enum"] = enum_values

        return schema


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


def _enum_to_values(enum_type):
    """
    Convert an Enum into a list of values
    """
    return [enum_attribute.value for enum_attribute in enum_type]

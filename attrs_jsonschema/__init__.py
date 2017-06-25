import attr
from .compat import string_type
from .exceptions import UnextractableSchema
from collections import OrderedDict
from attr.validators import (
    _InstanceOfValidator, _OptionalValidator,
    _AndValidator
)
from attr.exceptions import (
    NotAnAttrsClassError
)

schema_by_type = OrderedDict()
schema_by_type[bool] = {"type": "boolean"}
schema_by_type[int] = {"type": "integer"}
schema_by_type[string_type] = {"type": "string"}


def extract(attrs_or_primitive):
    """
    extract a jsonschema out of a primitive, or a attr object.
    """
    try:
        return extract_schema(attrs_or_primitive)
    except NotAnAttrsClassError:
        for typ, schema in schema_by_type.items():
            if issubclass(attrs_or_primitive, typ):
                return schema
    raise UnextractableSchema("type {0} is not an attrs or a primitive data type".format(
        attrs_or_primitive
    ))

def extract_schema(attrs_class):
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


@attr.s
class AttributeDetails(object):
    name = attr.ib()
    schema = attr.ib()
    is_required = attr.ib()

def extract_attribute(attribute):
    is_required = attribute.default is attr.NOTHING

    schema = None
    for validator in _iterate_validator(attribute.validator):
        if isinstance(validator, _InstanceOfValidator):
            schema = extract(validator.type)

    if schema is None:
        raise UnextractableSchema(
            "all attributes must have an 'InstanceOfValidator'. attribute {0} does not.".format(attribute)
        )
    return AttributeDetails(
        attribute.name, schema,  is_required
    )

def _iterate_validator(validator):
    if isinstance(validator, _AndValidator):
        for sub_validator in validator._validators:
            yield sub_validator
    else:
        yield validator

import attr
from .compat import string_type
from .exceptions import UnextractableSchema
from collections import OrderedDict
from attr.validators import (
    _InstanceOfValidator, _OptionalValidator,
    _AndValidator
)
from schema_extractor import DEFAULT_EXTRACTOR
from .fields import (
    boolean, integer, string
)

def extract_jsonschema(typ):
    return DEFAULT_EXTRACTOR.extract(typ)

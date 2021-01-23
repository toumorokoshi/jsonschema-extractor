import attr
from typing import Optional

import pytest

from jsonschema_extractor import UnextractableSchema

POSSIBLE_OPTIONS = ['option1', 'option2']


@attr.s
class Example(object):
    options = attr.ib(type=str, validator=attr.validators.in_(POSSIBLE_OPTIONS))


@attr.s
class ExampleWithoutType(object):
    options = attr.ib(validator=attr.validators.in_(POSSIBLE_OPTIONS))


@attr.s
class ExampleWithBrokenSchema(object):
    foo = attr.ib()
    options = attr.ib(validator=attr.validators.in_(POSSIBLE_OPTIONS))


@attr.s
class ExampleWithTuple(object):
    options = attr.ib(type=str, validator=attr.validators.in_(set(POSSIBLE_OPTIONS)))


@pytest.mark.parametrize('example_class', [Example, ExampleWithTuple])
def test_in_validator_happy_flow(extractor, example_class):
    expected_schema = {
        'properties': {
            'options': {
                'type': 'string',
                'enum': POSSIBLE_OPTIONS
            }
        },
        'required': ['options'],
        'title': example_class.__name__,
        'type': 'object'
    }

    assert expected_schema == extractor.extract(example_class)


def test_in_validator_without_type(extractor):
    expected_schema = {
        'properties': {
            'options': {
                'enum': POSSIBLE_OPTIONS
            }
        },
        'required': ['options'],
        'title': 'ExampleWithoutType',
        'type': 'object'
    }

    assert expected_schema == extractor.extract(ExampleWithoutType)


def test_in_validator_with_broken_schema(extractor):
    with pytest.raises(UnextractableSchema):
        assert extractor.extract(ExampleWithBrokenSchema)

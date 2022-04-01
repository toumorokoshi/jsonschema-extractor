====================
jsonschema-extractor
====================

jsonschema-extractor is a library and extensible framework for
extracting `json schema <http://json-schema.org/>`_ from various object and
primitives.

.. image:: https://github.com/toumorokoshi/jsonschema-extractor/actions/workflows/python-package.yaml/badge.svg
    :target: https://github.com/toumorokoshi/jsonschema-extractor/actions/workflows/python-package.yaml

Out of the box support exists for:

- `attrs <https://attrs.readthedocs.io/>`_
- `typing <https://docs.python.org/3/library/typing.html>`_

-----
Usage
-----

.. code-block:: python


    from typing import List
    import jsonschema_extractor
    assert jsonschema_extractor.extract(List[int]) == {
        "type": "array",
        "items": {"type": "integer"}
    }


-------------
Attrs-example
-------------

.. code-block:: python

    import attr
    from attr.validators import instance_of
    import jsonschema_extractor

    @attr.define
    class Example(object):
        integer: int = attr.field()
        foo = attr.field(metadata={"jsonschema": {"type": "string", "format": "uuid"}})
        validator_list: List[float] = attr.field()
        string: str = attr.field(
            default="foo",
            metadata={"description": "This is an description."}
        )

    assert extractor.extract(Example) == {
        "type": "object",
        "title": "Example",
        "properties": {
            "string": {"description": "This is an description.", "type": "string"},
            "integer": {"type": "integer"},
            "validator_list": {"items": {"type": "number"}, "type": "array"},
            "foo": {"type": "string", "format": "uuid"},
        },
        "required": ["integer", "foo", "validator_list"],
    }


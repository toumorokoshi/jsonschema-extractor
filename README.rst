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

import pytest
from jsonschema_extractor import init_default_extractor


@pytest.fixture
def extractor():
    return init_default_extractor()

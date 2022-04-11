import pytest
from aioresponses import aioresponses


@pytest.fixture
def mocked():
    """Mock/fake web requests in python aiohttp package."""
    with aioresponses() as mock:
        yield mock

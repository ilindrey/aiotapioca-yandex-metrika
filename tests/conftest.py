import pytest
from aioresponses import aioresponses
from async_solipsism import EventLoop  # type: ignore


@pytest.fixture
def mocked():
    """Mock/fake web requests in python aiohttp package."""
    with aioresponses() as mock:
        yield mock


@pytest.fixture
def event_loop():
    loop = EventLoop()
    yield loop
    loop.close()

from fastapi.testclient import TestClient
from pytest import fixture

from main import app


@fixture
def anyio_backend():
    return "asyncio"


@fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

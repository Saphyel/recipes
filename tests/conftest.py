from pytest import fixture


@fixture
def anyio_backend():
    return "asyncio"

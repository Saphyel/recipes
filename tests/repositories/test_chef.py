from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.chef import Chef
from repositories.chef import chef_repository
from schemas import ChefCreate, ChefUpdate


@mark.asyncio
class TestChefRepository:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Chef(name="pepe")])])
    async def test_list(self, offset: int, limit: int, expect: List[Chef]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.all.return_value = expect
        assert await chef_repository.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("pepe", Chef(name="pepe"))])
    async def test_find(self, param: str, expect: Chef) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = expect
        assert await chef_repository.find(session, name=param) == expect

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(["payload", "expect"], [(ChefCreate(name="pepe"), Chef(name="pepe"))])
    async def test_create(self, payload: ChefCreate, expect: Chef) -> None:
        assert await chef_repository.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await chef_repository.remove(AsyncMock(), model=Chef(name="pepe")) is None

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(
        ["entity", "payload", "expect"],
        [(Chef(name="pepe"), ChefUpdate(reddit="espepe"), Chef(name="pepe", reddit="espepe"))],
    )
    async def test_update(self, entity: Chef, payload: ChefUpdate, expect: Chef) -> None:
        assert await chef_repository.update(AsyncMock(), db_obj=entity, obj_in=payload) == expect

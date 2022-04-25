from typing import List
from unittest.mock import AsyncMock, Mock

from pytest import mark

from models.chef import Chef
from repositories.chef import ChefRepository
from schemas import ChefCreate, ChefUpdate


@mark.anyio
class TestChefRepository:
    @mark.parametrize("expect", ([], [Chef(name="pepe")]))
    async def test_list(self, expect: List[Chef]) -> None:
        result = Mock()
        result.unique.return_value.scalars.return_value.all.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await ChefRepository(session).list() == expect

    @mark.parametrize(["param", "expect"], [("pepe", Chef(name="pepe"))])
    async def test_find(self, param: str, expect: Chef) -> None:
        result = Mock()
        result.unique.return_value.scalar_one.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await ChefRepository(session).find(name=param) == expect

    @mark.parametrize(["payload", "expect"], [(ChefCreate(name="pepe"), Chef(name="pepe"))])
    async def test_create(self, payload: ChefCreate, expect: Chef) -> None:
        result = Mock()
        result.scalar_one.return_value = expect.name
        session = AsyncMock()
        session.execute.return_value = result
        assert await ChefRepository(session).create(obj_in=payload) == expect.name

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await ChefRepository(session).remove(chef=Chef(name="pepe")) is None

    @mark.parametrize(["name", "payload"], [("pepe", ChefUpdate(reddit="espepe"))])
    async def test_update(self, name: str, payload: ChefUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = name
        assert await ChefRepository(session).update(name=name, obj_in=payload) is None

from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.chef import Chef
from repositories.chef import chef_repository
from schemas import ChefCreate, ChefUpdate


@mark.anyio
class TestChefRepository:
    @mark.parametrize(["result", "expect"], [([], []), ([{"name": "pepe"}], [Chef(name="pepe")])])
    async def test_list(self, result: List[dict], expect: List[Chef]) -> None:
        session = AsyncMock()
        session.fetch_all.return_value = result
        assert await chef_repository.list(session) == expect

    @mark.parametrize(["param", "expect"], [("pepe", {"name": "pepe"})])
    async def test_find(self, param: str, expect: dict) -> None:
        session = AsyncMock()
        session.fetch_one.return_value = expect
        assert await chef_repository.find(session, name=param) == Chef(**expect)

    @mark.parametrize(["payload", "expect"], [(ChefCreate(name="pepe"), Chef(name="pepe"))])
    async def test_create(self, payload: ChefCreate, expect: Chef) -> None:
        session = AsyncMock()
        session.execute.return_value = expect
        assert await chef_repository.create(session, obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await chef_repository.remove(session, name="pepe") is None

    @mark.parametrize(["name", "payload"], [("pepe", ChefUpdate(reddit="espepe"))])
    async def test_update(self, name: str, payload: ChefUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = name
        assert await chef_repository.update(session, name=name, obj_in=payload) is None

from typing import List
from unittest.mock import AsyncMock

import pytest
from pytest import mark
from sqlalchemy.exc import IntegrityError

from crud import chef
from models.chef import Chef
from schemas import ChefCreate, ChefUpdate


@mark.asyncio
class TestCRUDChef:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Chef(name="pepe")])])
    async def test_list(self, offset: int, limit: int, expect: List[Chef]):
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.all.return_value = expect
        assert await chef.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", IntegrityError), ("pepe", Chef(name="pepe"))])
    async def test_get(self, param: str, expect):
        if type(expect) == Chef:
            session = AsyncMock()
            session.execute.return_value.scalars.return_value.one.return_value = expect
            assert await chef.get(session, name=param) == expect
        else:
            session = AsyncMock(side_effect=expect)
            session.execute.return_value.scalars.return_value.one.side_effect = expect("h", [], Exception)
            with pytest.raises(expect):
                await chef.get(session, name=param)

    @mark.parametrize(["payload", "expect"], [(ChefCreate(name="pepe"), Chef(name="pepe"))])
    async def test_create(self, payload: ChefCreate, expect: Chef):
        assert await chef.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self):
        assert await chef.remove(AsyncMock(), model=Chef(name="pepe")) is None  # type: ignore

    @mark.parametrize(
        ["entity", "payload", "expect"],
        [(Chef(name="pepe"), ChefUpdate(reddit="espepe"), Chef(name="pepe", reddit="espepe"))],
    )
    async def test_update(self, entity: Chef, payload: ChefUpdate, expect: Chef):
        assert await chef.update(AsyncMock(), db_obj=entity, obj_in=payload) == expect

from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.category import Category
from repositories.category import CategoryRepository
from schemas import CategoryCreate


@mark.anyio
class TestCategoryRepository:
    @mark.parametrize(["result", "expect"], [([], []), ([{"name": "sandwich"}], [Category(name="sandwich")])])
    async def test_list(self, result: List[dict], expect: List[Category]) -> None:
        session = AsyncMock()
        session.fetch_all.return_value = result
        assert await CategoryRepository().list(session) == expect

    @mark.parametrize(["param", "expect"], [("sandwich", {"name": "sandwich"})])
    async def test_find(self, param: str, expect: dict) -> None:
        session = AsyncMock()
        session.fetch_one.return_value = expect
        assert await CategoryRepository().find(session, name=param) == Category(**expect)

    @mark.parametrize(["payload", "expect"], [(CategoryCreate(name="sandwich"), "sandwich")])
    async def test_create(self, payload: CategoryCreate, expect: str) -> None:
        session = AsyncMock()
        session.execute.return_value = expect
        assert await CategoryRepository().create(session, obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await CategoryRepository().remove(session, name="sandwich") is None

from typing import List
from unittest.mock import AsyncMock, Mock

from pytest import mark

from models.category import Category
from repositories.category import CategoryRepository
from schemas import CategoryCreate


@mark.anyio
class TestCategoryRepository:
    @mark.parametrize("expect", ([], Category(name="sandwich")))
    async def test_list(self, expect: List[Category]) -> None:
        result = Mock()
        result.unique.return_value.scalars.return_value.all.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await CategoryRepository(session).list() == expect

    @mark.parametrize(["param", "expect"], [("sandwich", Category(name="sandwich"))])
    async def test_find(self, param: str, expect: Category) -> None:
        result = Mock()
        result.unique.return_value.scalar_one.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await CategoryRepository(session).find(name=param) == expect

    @mark.parametrize(["payload", "expect"], [(CategoryCreate(name="sandwich"), Category(name="sandwich"))])
    async def test_create(self, payload: CategoryCreate, expect: Category) -> None:
        # result = Mock()
        # result.scalar_one.return_value = expect
        session = AsyncMock()
        assert await CategoryRepository(session).create(obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await CategoryRepository(session).remove(category=Category(name="sandwich")) is None

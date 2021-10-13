from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from crud import category
from models.category import Category
from schemas import CategoryCreate


@mark.asyncio
class TestCRUDCategory:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Category(name="sandwich")])])
    async def test_list(self, offset: int, limit: int, expect: List[Category]) -> None:
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.all.return_value = expect
        assert await category.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Category(name="sandwich"))])
    async def test_get(self, param: str, expect: Optional[Category]) -> None:
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.one.return_value = expect
        assert await category.get(session, name=param) == expect

    @mark.parametrize(["payload", "expect"], [(CategoryCreate(name="sandwich"), Category(name="sandwich"))])
    async def test_create(self, payload: CategoryCreate, expect: Category) -> None:
        assert await category.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await category.remove(AsyncMock(), model=Category(name="sandwich")) is None  # type: ignore

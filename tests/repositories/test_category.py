from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from models.category import Category
from repositories.category import category_repository
from schemas import CategoryCreate


@mark.asyncio
class TestCategoryRepository:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Category(name="sandwich")])])
    async def test_list(self, offset: int, limit: int, expect: List[Category]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.all.return_value = expect
        assert await category_repository.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Category(name="sandwich"))])
    async def test_find(self, param: str, expect: Optional[Category]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = expect
        assert await category_repository.find(session, name=param) == expect

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(["payload", "expect"], [(CategoryCreate(name="sandwich"), Category(name="sandwich"))])
    async def test_create(self, payload: CategoryCreate, expect: Category) -> None:
        assert await category_repository.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await category_repository.remove(AsyncMock(), model=Category(name="sandwich")) is None

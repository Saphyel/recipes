from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from models.ingredient import Ingredient
from repositories.ingredient import ingredient_repository
from schemas import IngredientCreate


@mark.asyncio
class TestIngredientRepository:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Ingredient(name="sandwich")])])
    async def test_list(self, offset: int, limit: int, expect: List[Ingredient]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.all.return_value = expect
        assert await ingredient_repository.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Ingredient(name="sandwich"))])
    async def test_find(self, param: str, expect: Optional[Ingredient]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = expect
        assert await ingredient_repository.find(session, name=param) == expect

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(["payload", "expect"], [(IngredientCreate(name="sandwich"), Ingredient(name="sandwich"))])
    async def test_create(self, payload: IngredientCreate, expect: Ingredient) -> None:
        assert await ingredient_repository.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await ingredient_repository.remove(AsyncMock(), model=Ingredient(name="sandwich")) is None

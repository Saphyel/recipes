from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from crud import ingredient
from models.ingredient import Ingredient
from schemas import IngredientCreate


@mark.asyncio
class TestCRUDIngredient:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Ingredient(name="sandwich")])])
    async def test_list(self, offset: int, limit: int, expect: List[Ingredient]) -> None:
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.all.return_value = expect
        assert await ingredient.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Ingredient(name="sandwich"))])
    async def test_get(self, param: str, expect: Optional[Ingredient]) -> None:
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.one.return_value = expect
        assert await ingredient.get(session, name=param) == expect

    @mark.parametrize(["payload", "expect"], [(IngredientCreate(name="sandwich"), Ingredient(name="sandwich"))])
    async def test_create(self, payload: IngredientCreate, expect: Ingredient) -> None:
        assert await ingredient.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await ingredient.remove(AsyncMock(), model=Ingredient(name="sandwich")) is None  # type: ignore

from typing import List
from unittest.mock import AsyncMock, Mock

from pytest import mark

from models.ingredient import Ingredient
from repositories.ingredient import IngredientRepository
from schemas import IngredientCreate


@mark.anyio
class TestIngredientRepository:
    @mark.parametrize("expect", ([], [Ingredient(name="sandwich")]))
    async def test_list(self, expect: List[Ingredient]) -> None:
        result = Mock()
        result.scalars.return_value.all.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await IngredientRepository(session).list() == expect

    @mark.parametrize(["param", "expect"], [("sandwich", Ingredient(name="sandwich"))])
    async def test_find(self, param: str, expect: dict) -> None:
        result = Mock()
        result.scalar_one.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await IngredientRepository(session).find(name=param) == expect

    @mark.parametrize(["payload", "expect"], [(IngredientCreate(name="sandwich"), Ingredient(name="sandwich"))])
    async def test_create(self, payload: IngredientCreate, expect: Ingredient) -> None:
        result = Mock()
        result.scalar_one.return_value = expect.name
        session = AsyncMock()
        session.execute.return_value = result
        assert await IngredientRepository(session).create(obj_in=payload) == expect.name

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await IngredientRepository(session).remove(ingredient=Ingredient(name="sandwich")) is None

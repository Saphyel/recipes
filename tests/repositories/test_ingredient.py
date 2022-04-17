from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.ingredient import Ingredient
from repositories.ingredient import IngredientRepository
from schemas import IngredientCreate


@mark.anyio
class TestIngredientRepository:
    @mark.parametrize(["result", "expect"], [([], []), ([{"name": "sandwich"}], [Ingredient(name="sandwich")])])
    async def test_list(self, result: List[dict], expect: List[Ingredient]) -> None:
        session = AsyncMock()
        session.fetch_all.return_value = result
        assert await IngredientRepository().list(session) == expect

    @mark.parametrize(["param", "expect"], [("sandwich", {"name": "sandwich"})])
    async def test_find(self, param: str, expect: dict) -> None:
        session = AsyncMock()
        session.fetch_one.return_value = expect
        assert await IngredientRepository().find(session, name=param) == Ingredient(**expect)

    @mark.parametrize(["payload", "expect"], [(IngredientCreate(name="sandwich"), Ingredient(name="sandwich"))])
    async def test_create(self, payload: IngredientCreate, expect: Ingredient) -> None:
        session = AsyncMock()
        session.execute.return_value = expect
        assert await IngredientRepository().create(session, obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await IngredientRepository().remove(session, name="sandwich") is None

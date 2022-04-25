from typing import List
from unittest.mock import AsyncMock, Mock

from pytest import mark

from models.recipe import Recipe
from repositories.recipe import RecipeRepository
from schemas import RecipeCreate, RecipeUpdate


@mark.anyio
class TestRecipeRepository:
    @mark.parametrize("expect", ([], [Recipe(title="sandwich")]))
    async def test_list(self, expect: List[Recipe]) -> None:
        result = Mock()
        result.unique.return_value.scalars.return_value.all.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await RecipeRepository(session).list() == expect

    @mark.parametrize(["param", "expect"], [("sandwich", Recipe(title="sandwich"))])
    async def test_find(self, param: str, expect: dict) -> None:
        result = Mock()
        result.unique.return_value.scalar_one.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await RecipeRepository(session).find(title=param) == expect

    @mark.parametrize(["payload", "expect"], [(RecipeCreate(title="sandwich"), Recipe(title="sandwich"))])
    async def test_create(self, payload: RecipeCreate, expect: Recipe) -> None:
        result = Mock()
        result.scalar_one.return_value = expect.title
        session = AsyncMock()
        session.execute.return_value = result
        assert await RecipeRepository(session).create(obj_in=payload) == expect.title

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await RecipeRepository(session).remove(recipe=Recipe(title="sandwich")) is None

    @mark.parametrize(["title", "payload"], [("sandwich", RecipeUpdate(active_cook=3))])
    async def test_update(self, title: str, payload: RecipeUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = title
        assert await RecipeRepository(session).update(title=title, obj_in=payload) is None

from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.recipe import Recipe
from repositories.recipe import recipe_repository
from schemas import RecipeCreate, RecipeUpdate


@mark.anyio
class TestRecipeRepository:
    @mark.parametrize(
        ["result", "category", "expect"],
        [([], None, []), ([{"title": "sandwich"}], "cena", [Recipe(title="sandwich")])],
    )
    async def test_list(self, result: List[dict], category: str, expect: List[Recipe]) -> None:
        session = AsyncMock()
        session.fetch_all.return_value = result
        assert await recipe_repository.list(session, category=category) == expect

    @mark.parametrize(["param", "expect"], [("sandwich", {"title": "sandwich"})])
    async def test_find(self, param: str, expect: dict) -> None:
        session = AsyncMock()
        session.fetch_one.return_value = expect
        assert await recipe_repository.find(session, title=param) == Recipe(**expect)

    @mark.parametrize(["payload", "expect"], [(RecipeCreate(title="sandwich"), Recipe(title="sandwich"))])
    async def test_create(self, payload: RecipeCreate, expect: Recipe) -> None:
        session = AsyncMock()
        session.execute.return_value = expect
        assert await recipe_repository.create(session, obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await recipe_repository.remove(session, title="sandwich") is None

    @mark.parametrize(["title", "payload"], [("sandwich", RecipeUpdate(active_cook=3))])
    async def test_update(self, title: str, payload: RecipeUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = title
        assert await recipe_repository.update(session, title=title, obj_in=payload) is None

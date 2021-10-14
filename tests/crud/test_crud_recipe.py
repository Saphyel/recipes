from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from crud import recipe
from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


@mark.asyncio
class TestCRUDRecipe:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Recipe(title="sandwich")])])
    async def test_list(self, offset: int, limit: int, expect: List[Recipe]):
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.all.return_value = expect
        assert await recipe.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Recipe(title="sandwich"))])
    async def test_get(self, param: str, expect: Optional[Recipe]):
        session = AsyncMock()
        session.execute.return_value.scalars.return_value.one.return_value = expect
        assert await recipe.get(session, title=param) == expect

    @mark.parametrize(["payload", "expect"], [(RecipeCreate(title="sandwich"), Recipe(title="sandwich"))])
    async def test_create(self, payload: RecipeCreate, expect: Recipe):
        assert await recipe.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self):
        assert await recipe.remove(AsyncMock(), model=Recipe(title="sandwich")) is None  # type: ignore

    @mark.parametrize(
        ["entity", "payload", "expect"],
        [(Recipe(title="sandwich"), RecipeUpdate(active_cook=3), Recipe(title="sandwich", active_cook=3))],
    )
    async def test_update(self, entity: Recipe, payload: RecipeUpdate, expect: Recipe):
        assert await recipe.update(AsyncMock(), db_obj=entity, obj_in=payload) == expect

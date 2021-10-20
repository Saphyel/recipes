from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from models.recipe import Recipe
from repositories.recipe import recipe_repository
from schemas import RecipeCreate, RecipeUpdate


@mark.asyncio
class TestRecipeRepository:
    @mark.parametrize(
        ["offset", "limit", "category", "expect"], [(0, 5, None, []), (1, 1, "cena", [Recipe(title="sandwich")])]
    )
    async def test_list(self, offset: int, limit: int, category: str, expect: List[Recipe]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.all.return_value = expect
        assert await recipe_repository.list(session, offset=offset, limit=limit, category=category) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Recipe(title="sandwich"))])
    async def test_find(self, param: str, expect: Optional[Recipe]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = expect
        assert await recipe_repository.find(session, title=param) == expect

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(["payload", "expect"], [(RecipeCreate(title="sandwich"), Recipe(title="sandwich"))])
    async def test_create(self, payload: RecipeCreate, expect: Recipe) -> None:
        assert await recipe_repository.create(AsyncMock(), obj_in=payload) == expect

    async def test_remove(self) -> None:
        assert await recipe_repository.remove(AsyncMock(), model=Recipe(title="sandwich")) is None

    @mark.parametrize(
        ["entity", "payload", "expect"],
        [(Recipe(title="sandwich"), RecipeUpdate(active_cook=3), Recipe(title="sandwich", active_cook=3))],
    )
    async def test_update(self, entity: Recipe, payload: RecipeUpdate, expect: Recipe) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = entity
        await recipe_repository.update(session, db_obj=entity, obj_in=payload)
        assert entity == expect

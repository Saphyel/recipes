from typing import Optional, List
from unittest.mock import Mock

import pytest

from crud import recipe
from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


class TestCRUDRecipe:
    @pytest.mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Recipe(title="sandwich"))])
    def test_get(self, param: str, expect: Optional[Recipe]):
        session = Mock()
        session.query.return_value.filter.return_value.one.return_value = expect
        assert recipe.get(session, title=param) == expect

    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Recipe(title="sandwich")])])
    def test_list(self, offset: int, limit: int, expect: List[Recipe]):
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert recipe.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["payload", "expect"], [(RecipeCreate(title="sandwich"), Recipe(title="sandwich"))])
    def test_create(self, payload: RecipeCreate, expect: Recipe):
        result = recipe.create(Mock(), obj_in=payload)
        assert result.title == expect.title

    @pytest.mark.parametrize(["param", "expect"], [(Recipe(title="sandwich"), None)])
    def test_remove(self, param: Recipe, expect: Optional[str]):
        session = Mock()
        assert recipe.remove(session, model=param) == expect

    @pytest.mark.parametrize(
        ["entity", "payload", "expect"],
        [
            (Recipe(title="sandwich"), RecipeUpdate(active_cook=3), Recipe(title="sandwich", active_cook=3))
        ]
    )
    def test_update(self, entity: Recipe, payload: RecipeUpdate, expect: Recipe):
        result = recipe.update(Mock(), db_obj=entity, obj_in=payload)
        assert result.active_cook == expect.active_cook

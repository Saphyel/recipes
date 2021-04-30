from typing import Optional, List
from unittest.mock import Mock

import pytest

from crud import ingredient
from models.ingredient import Ingredient
from schemas import IngredientCreate


class TestCRUDIngredient:
    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Ingredient(name="sandwich")])])
    def test_list(self, offset: int, limit: int, expect: List[Ingredient]) -> None:
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert ingredient.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Ingredient(name="sandwich"))])
    def test_get(self, param: str, expect: Optional[Ingredient]) -> None:
        session = Mock()
        session.query.return_value.filter.return_value.one.return_value = expect
        assert ingredient.get(session, name=param) == expect

    @pytest.mark.parametrize(["payload", "expect"], [(IngredientCreate(name="sandwich"), Ingredient(name="sandwich"))])
    def test_create(self, payload: IngredientCreate, expect: Ingredient) -> None:
        assert ingredient.create(Mock(), obj_in=payload) == expect

    def test_remove(self) -> None:
        session = Mock()
        assert ingredient.remove(session, model=Ingredient(name="sandwich")) is None  # type: ignore

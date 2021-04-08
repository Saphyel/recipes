from typing import Optional, List
from unittest.mock import Mock

import pytest

from crud import category
from models.category import Category
from schemas import CategoryCreate


class TestCRUDCategory:
    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Category(name="sandwich")])])
    def test_list(self, offset: int, limit: int, expect: List[Category]) -> None:
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert category.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", Category(name="sandwich"))])
    def test_get(self, param: str, expect: Optional[Category]) -> None:
        session = Mock()
        session.query.return_value.filter.return_value.one.return_value = expect
        assert category.get(session, name=param) == expect

    @pytest.mark.parametrize(["payload", "expect"], [(CategoryCreate(name="sandwich"), Category(name="sandwich"))])
    def test_create(self, payload: CategoryCreate, expect: Category) -> None:
        assert category.create(Mock(), obj_in=payload) == expect

    def test_remove(self) -> None:
        session = Mock()
        assert category.remove(session, model=Category(name="sandwich")) is None  # type: ignore

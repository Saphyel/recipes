from typing import Optional, List
from unittest.mock import Mock

import pytest

from crud import user
from models.user import User
from schemas import UserCreate, UserUpdate


class TestCRUDUser:
    @pytest.mark.parametrize(["param", "expect"], [("hola", None), ("pepe", User(name="pepe"))])
    def test_get(self, param: str, expect: Optional[User]):
        session = Mock()
        session.query.return_value.filter.return_value.one.return_value = expect
        assert user.get(session, name=param) == expect

    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [User(name="pepe")])])
    def test_list(self, offset: int, limit: int, expect: List[User]):
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert user.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["payload", "expect"], [(UserCreate(name="pepe"), User(name="pepe"))])
    def test_create(self, payload: UserCreate, expect: User):
        result = user.create(Mock(), obj_in=payload)
        assert result.name == expect.name

    @pytest.mark.parametrize(["param", "expect"], [(User(name="pepe"), None)])
    def test_remove(self, param: User, expect: Optional[str]):
        session = Mock()
        assert user.remove(session, model=param) == expect

    @pytest.mark.parametrize(
        ["entity", "payload", "expect"],
        [
            (User(name="pepe"), UserUpdate(reddit="espepe"), User(name="pepe", reddit="espepe"))
        ]
    )
    def test_update(self, entity: User, payload: UserUpdate, expect: User):
        result = user.update(Mock(), db_obj=entity, obj_in=payload)
        assert result.reddit == expect.reddit

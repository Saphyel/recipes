from typing import List
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from crud import user
from models.user import User
from schemas import UserCreate, UserUpdate


class TestCRUDUser:
    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [User(name="pepe")])])
    def test_list(self, offset: int, limit: int, expect: List[User]):
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert user.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["param", "expect"], [("hola", IntegrityError), ("pepe", User(name="pepe"))])
    def test_get(self, param: str, expect):
        if type(expect) == User:
            session = Mock()
            session.query.return_value.filter.return_value.one.return_value = expect
            assert user.get(session, name=param) == expect
        else:
            session = Mock(side_effect=expect)
            session.query.return_value.filter.return_value.one.side_effect = expect("h", [], Exception)
            with pytest.raises(expect):
                user.get(session, name=param)

    @pytest.mark.parametrize(["payload", "expect"], [(UserCreate(name="pepe"), User(name="pepe"))])
    def test_create(self, payload: UserCreate, expect: User):
        session = Mock()
        assert user.create(session, obj_in=payload) == expect

    def test_remove(self):
        session = Mock()
        assert user.remove(session, model=User(name="pepe")) is None  # type: ignore

    @pytest.mark.parametrize(
        ["entity", "payload", "expect"],
        [(User(name="pepe"), UserUpdate(reddit="espepe"), User(name="pepe", reddit="espepe"))],
    )
    def test_update(self, entity: User, payload: UserUpdate, expect: User):
        session = Mock()
        assert user.update(session, db_obj=entity, obj_in=payload) == expect

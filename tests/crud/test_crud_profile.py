from typing import List
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from crud import profile
from models.profile import Profile
from schemas import ProfileCreate, ProfileUpdate


class TestCRUDProfile:
    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Profile(name="pepe")])])
    def test_list(self, offset: int, limit: int, expect: List[Profile]):
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert profile.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["param", "expect"], [("hola", IntegrityError), ("pepe", Profile(name="pepe"))])
    def test_get(self, param: str, expect):
        if type(expect) == Profile:
            session = Mock()
            session.query.return_value.filter.return_value.one.return_value = expect
            assert profile.get(session, name=param) == expect
        else:
            session = Mock(side_effect=expect)
            session.query.return_value.filter.return_value.one.side_effect = expect("h", [], Exception)
            with pytest.raises(expect):
                profile.get(session, name=param)

    @pytest.mark.parametrize(["payload", "expect"], [(ProfileCreate(name="pepe"), Profile(name="pepe"))])
    def test_create(self, payload: ProfileCreate, expect: Profile):
        session = Mock()
        assert profile.create(session, obj_in=payload) == expect

    def test_remove(self):
        session = Mock()
        assert profile.remove(session, model=Profile(name="pepe")) is None  # type: ignore

    @pytest.mark.parametrize(
        ["entity", "payload", "expect"],
        [(Profile(name="pepe"), ProfileUpdate(reddit="espepe"), Profile(name="pepe", reddit="espepe"))],
    )
    def test_update(self, entity: Profile, payload: ProfileUpdate, expect: Profile):
        session = Mock()
        assert profile.update(session, db_obj=entity, obj_in=payload) == expect

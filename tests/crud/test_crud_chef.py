from typing import List
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from crud import chef
from models.chef import Chef
from schemas import ChefCreate, ChefUpdate


class TestCRUDChef:
    @pytest.mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [Chef(name="pepe")])])
    def test_list(self, offset: int, limit: int, expect: List[Chef]):
        session = Mock()
        session.query.return_value.offset.return_value.limit.return_value = expect
        assert chef.list(session, offset=offset, limit=limit) == expect

    @pytest.mark.parametrize(["param", "expect"], [("hola", IntegrityError), ("pepe", Chef(name="pepe"))])
    def test_get(self, param: str, expect):
        if type(expect) == Chef:
            session = Mock()
            session.query.return_value.filter.return_value.one.return_value = expect
            assert chef.get(session, name=param) == expect
        else:
            session = Mock(side_effect=expect)
            session.query.return_value.filter.return_value.one.side_effect = expect("h", [], Exception)
            with pytest.raises(expect):
                chef.get(session, name=param)

    @pytest.mark.parametrize(["payload", "expect"], [(ChefCreate(name="pepe"), Chef(name="pepe"))])
    def test_create(self, payload: ChefCreate, expect: Chef):
        session = Mock()
        assert chef.create(session, obj_in=payload) == expect

    def test_remove(self):
        session = Mock()
        assert chef.remove(session, model=Chef(name="pepe")) is None  # type: ignore

    @pytest.mark.parametrize(
        ["entity", "payload", "expect"],
        [(Chef(name="pepe"), ChefUpdate(reddit="espepe"), Chef(name="pepe", reddit="espepe"))],
    )
    def test_update(self, entity: Chef, payload: ChefUpdate, expect: Chef):
        session = Mock()
        assert chef.update(session, db_obj=entity, obj_in=payload) == expect

from typing import List
from unittest.mock import AsyncMock

from pytest import mark

from models.user import User
from repositories.user import user_repository
from schemas.user import UserCreate, UserUpdate


@mark.anyio
class TestUserRepository:
    @mark.parametrize(
        ["result", "expect"], [([], []), ([{"name": "pepe", "password": "loco"}], [User(name="pepe", password="loco")])]
    )
    async def test_list(self, result: List[dict], expect: List[User]) -> None:
        session = AsyncMock()
        session.fetch_all.return_value = result
        assert await user_repository.list(session) == expect

    @mark.parametrize(["param", "expect"], [("pepe", {"name": "pepe", "password": "loco"})])
    async def test_find(self, param: str, expect: dict) -> None:
        session = AsyncMock()
        session.fetch_one.return_value = expect
        assert await user_repository.find(session, name=param) == User(**expect)

    @mark.parametrize(["payload", "expect"], [(UserCreate(name="pepe", password="loco"), "pepe")])
    async def test_create(self, payload: UserCreate, expect: str) -> None:
        session = AsyncMock()
        session.execute.return_value = expect
        assert await user_repository.create(session, obj_in=payload) == expect

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await user_repository.remove(session, name="sandwich") is None

    @mark.parametrize(["name", "payload"], [("pepe", UserUpdate(password="noche"))])
    async def test_update(self, name: str, payload: UserUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = name
        assert await user_repository.update(session, name=name, obj_in=payload) is None

    async def test_authenticate(self) -> None:
        assert (
            await user_repository.authenticate(
                db_obj=User(
                    name="pepe",
                    password="$argon2id$v=19$m=102400,t=2,p=8$PAegdO59b815zxmD0BojBA$1MYJQ4fiJ9IaWafW5pTYGw",
                ),
                password="loco",
            )
            is True
        )

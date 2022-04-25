from typing import List
from unittest.mock import AsyncMock, Mock

from pytest import mark

from models.user import User
from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate


@mark.anyio
class TestUserRepository:
    @mark.parametrize("expect", ([], [User(name="pepe", password="loco")]))
    async def test_list(self, expect: List[User]) -> None:
        result = Mock()
        result.scalars.return_value.all.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await UserRepository(session).list() == expect

    @mark.parametrize(["param", "expect"], [("pepe", User(name="pepe", password="loco"))])
    async def test_find(self, param: str, expect: User) -> None:
        result = Mock()
        result.scalar_one.return_value = expect
        session = AsyncMock()
        session.execute.return_value = result
        assert await UserRepository(session).find(name=param) == expect

    @mark.parametrize(
        ["payload", "expect"], [(UserCreate(name="pepe", password="loco"), User(name="pepe", password="loco"))]
    )
    async def test_create(self, payload: UserCreate, expect: User) -> None:
        result = Mock()
        result.scalar_one.return_value = expect.name
        session = AsyncMock()
        session.execute.return_value = result
        assert await UserRepository(session).create(obj_in=payload) == expect.name

    async def test_remove(self) -> None:
        session = AsyncMock()
        session.execute.return_value = "expect"
        assert await UserRepository(session).remove(user=User(name="pepe", password="loco")) is None

    @mark.parametrize(["name", "payload"], [("pepe", UserUpdate(password="noche"))])
    async def test_update(self, name: str, payload: UserUpdate) -> None:
        session = AsyncMock()
        session.execute.return_value = name

        assert await UserRepository(session).update(name=name, obj_in=payload) is None

    async def test_authenticate(self) -> None:
        assert (
            await UserRepository().authenticate(
                db_obj=User(
                    name="pepe",
                    password="$argon2id$v=19$m=102400,t=2,p=8$PAegdO59b815zxmD0BojBA$1MYJQ4fiJ9IaWafW5pTYGw",
                ),
                password="loco",
            )
            is True
        )

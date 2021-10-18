from typing import Optional, List
from unittest.mock import AsyncMock

from pytest import mark

from models.user import User
from repositories.user import user_repository
from schemas import UserCreate


@mark.asyncio
class TestCategoryRepository:
    @mark.parametrize(["offset", "limit", "expect"], [(0, 5, []), (1, 1, [User(name="sandwich", password="loco")])])
    async def test_list(self, offset: int, limit: int, expect: List[User]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.all.return_value = expect
        assert await user_repository.list(session, offset=offset, limit=limit) == expect

    @mark.parametrize(["param", "expect"], [("hola", None), ("sandwich", User(name="sandwich", password="loco"))])
    async def test_find(self, param: str, expect: Optional[User]) -> None:
        session = AsyncMock()
        session.stream_scalars.return_value.one.return_value = expect
        assert await user_repository.find(session, name=param) == expect

    @mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call':RuntimeWarning")
    @mark.parametrize(["payload", "expect"], [(UserCreate(name="sandwich", password="loco"), "sandwich")])
    async def test_create(self, payload: UserCreate, expect: str) -> None:
        result = await user_repository.create(AsyncMock(), obj_in=payload)
        assert result.name == expect

    async def test_remove(self) -> None:
        assert await user_repository.remove(AsyncMock(), model=User(name="sandwich", password="loco")) is None

    async def test_authenticate(self) -> None:
        assert (
            await user_repository.authenticate(
                db_obj=User(
                    name="sandwich",
                    password="$argon2id$v=19$m=102400,t=2,p=8$PAegdO59b815zxmD0BojBA$1MYJQ4fiJ9IaWafW5pTYGw",
                ),
                password="loco",
            )
            is True
        )
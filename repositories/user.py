from typing import List

from core.config import pwd_context
from models.user import User
from schemas.user import UserCreate, UserUpdate
from sqlalchemy import select, insert, update
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def list(self, *, offset: int = 0, limit: int = 100) -> List[User]:
        query = select(User).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def find(self, *, name: str) -> User:
        query = select(User).where(User.name == name)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def authenticate(self, *, db_obj: User, password: str) -> bool:
        return pwd_context.verify(password, db_obj.password)

    async def create(self, *, obj_in: UserCreate) -> str:
        query = insert(User).values(name=obj_in.name, password=pwd_context.hash(obj_in.password)).returning(User.name)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def update(self, *, name: str, obj_in: UserUpdate) -> None:
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            update_data["password"] = pwd_context.hash(update_data["password"])
        query = update(User).where(User.name == name).values(update_data).returning(User.name)
        await self.db.execute(query)

    async def remove(self, *, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

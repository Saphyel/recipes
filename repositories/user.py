from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import pwd_context
from models.user import User
from repositories.base import BaseRepository
from schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> List[User]:
        result = await db.stream_scalars(select(User).offset(offset).limit(limit))
        return await result.all()

    async def find(self, db: AsyncSession, *, name: str) -> User:
        result = await db.stream_scalars(select(User).filter(User.name == name))
        return await result.one()

    async def authenticate(self, *, db_obj: User, password: str) -> bool:
        return pwd_context.verify(password, db_obj.password)

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(name=obj_in.name, password=pwd_context.hash(obj_in.password))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> None:
        obj_data = db_obj.__dict__
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            update_data["password"] = pwd_context.hash(update_data["password"])
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)


user_repository = UserRepository(User)

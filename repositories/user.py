from typing import List

from databases import Database
from sqlalchemy import select, insert, delete, update

from core.config import pwd_context
from models.user import User
from schemas.user import UserCreate, UserUpdate


class UserRepository:
    async def list(self, db: Database, *, offset: int = 0, limit: int = 100) -> List[User]:
        query = select(User).offset(offset).limit(limit)
        result = await db.fetch_all(query)
        return [User(**item) for item in result]  # type: ignore

    async def find(self, db: Database, *, name: str) -> User:
        query = select(User).where(User.name == name)
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return User(**result)  # type: ignore

    async def authenticate(self, *, db_obj: User, password: str) -> bool:
        return pwd_context.verify(password, db_obj.password)

    async def create(self, db: Database, *, obj_in: UserCreate) -> str:
        query = insert(User).values(name=obj_in.name, password=pwd_context.hash(obj_in.password)).returning(User.name)
        result = await db.execute(query)
        return result

    async def update(self, db: Database, *, name: str, obj_in: UserUpdate) -> None:
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            update_data["password"] = pwd_context.hash(update_data["password"])
        query = update(User).where(User.name == name).values(update_data).returning(User.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")

    async def remove(self, db: Database, *, name: str) -> None:
        query = delete(User).where(User.name == name).returning(User.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")

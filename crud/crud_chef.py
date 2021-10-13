from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.chef import Chef
from schemas import ChefCreate, ChefUpdate


class CRUDChef(CRUDBase[Chef, ChefCreate, ChefUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> Iterable[Chef]:
        result = await db.execute(select(self.model).offset(offset).limit(limit))
        result = await result.scalars()
        return await result.all()

    async def create(self, db: AsyncSession, *, obj_in: ChefCreate) -> Chef:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        await db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, name: str) -> Chef:
        result = await db.execute(select(self.model).filter(Chef.name == name))
        result = await result.scalars()
        return await result.one()


chef = CRUDChef(Chef)

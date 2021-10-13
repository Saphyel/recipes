from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> Iterable[Category]:
        result = await db.execute(select(self.model).offset(offset).limit(limit))
        result = await result.scalars()
        return await result.all()

    async def create(self, db: AsyncSession, *, obj_in: CategoryCreate) -> Category:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        await db.add(db_obj)
        await db.commit()
        return db_obj

    async def get(self, db: AsyncSession, *, name: str) -> Category:
        result = await db.execute(select(self.model).filter(Category.name == name))
        result = await result.scalars()
        return await result.one()


category = CRUDCategory(Category)

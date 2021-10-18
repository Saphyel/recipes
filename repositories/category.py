from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.category import Category
from repositories.base import BaseRepository
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> List[Category]:
        result = await db.stream_scalars(select(Category).offset(offset).limit(limit))
        return await result.all()

    async def find(self, db: AsyncSession, *, name: str) -> Category:
        result = await db.stream_scalars(select(Category).filter(Category.name == name))
        return await result.one()

    async def create(self, db: AsyncSession, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(**obj_in.__dict__)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        obj_data = db_obj.__dict__
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


category_repository = CategoryRepository(Category)
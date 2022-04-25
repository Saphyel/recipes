from typing import List

from models.category import Category
from schemas.category import CategoryCreate
from sqlalchemy import select
from .base import BaseRepository


class CategoryRepository(BaseRepository):
    async def list(self, *, offset: int = 0, limit: int = 100) -> List[Category]:
        query = select(Category).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def find(self, *, name: str) -> Category:
        query = select(Category).where(Category.name == name)
        result = await self.db.execute(query)
        return result.unique().scalar_one()

    async def create(self, *, obj_in: CategoryCreate) -> Category:
        result = Category(**obj_in.__dict__)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def remove(self, *, category: Category) -> None:
        await self.db.delete(category)
        await self.db.commit()

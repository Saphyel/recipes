from typing import List

from databases import Database
from sqlalchemy import select, insert, delete

from models.category import Category
from schemas.category import CategoryCreate


class CategoryRepository:
    async def list(self, db: Database, *, offset: int = 0, limit: int = 100) -> List[Category]:
        query = select(Category).offset(offset).limit(limit)
        result = await db.fetch_all(query)
        return [Category(**item) for item in result]

    async def find(self, db: Database, *, name: str) -> Category:
        query = select(Category).where(Category.name == name)
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return Category(**result)

    async def create(self, db: Database, *, obj_in: CategoryCreate) -> str:
        query = insert(Category).values(**obj_in.__dict__).returning(Category.name)
        return await db.execute(query)

    async def remove(self, db: Database, *, name: str) -> None:
        query = delete(Category).where(Category.name == name).returning(Category.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")


category_repository = CategoryRepository()

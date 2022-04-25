from typing import Optional, List

from .base import BaseRepository
from sqlalchemy import select, insert, update

from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


class RecipeRepository(BaseRepository):
    async def list(self, *, offset: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Recipe]:
        query = select(Recipe)

        if category:
            query = query.where(Recipe.category_name == category)

        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def find(self, *, title: str) -> Recipe:
        query = select(Recipe).where(Recipe.title == title)
        result = await self.db.execute(query)
        return result.unique().scalar_one()

    async def create(self, *, obj_in: RecipeCreate) -> str:
        query = insert(Recipe).values(**obj_in.__dict__).returning(Recipe.title)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def remove(self, *, recipe: Recipe) -> None:
        await self.db.delete(recipe)
        await self.db.commit()

    async def update(self, *, title: str, obj_in: RecipeUpdate) -> None:
        query = (
            update(Recipe)
            .where(Recipe.title == title)
            .values(**obj_in.dict(exclude_unset=True))
            .returning(Recipe.title)
        )
        await self.db.execute(query)

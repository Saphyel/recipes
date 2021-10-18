from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recipe import Recipe
from repositories.base import BaseRepository
from schemas import RecipeCreate, RecipeUpdate


class RecipeRepository(BaseRepository[Recipe, RecipeCreate, RecipeUpdate]):
    async def list(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100, category: Optional[str] = None
    ) -> List[Recipe]:
        query = select(Recipe)

        if category:
            query = query.filter(Recipe.category_name == category)

        result = await db.stream_scalars(query.offset(offset).limit(limit))
        return await result.all()

    async def find(self, db: AsyncSession, *, title: str) -> Recipe:
        result = await db.stream_scalars(select(Recipe).filter(Recipe.title == title))
        return await result.one()

    async def create(self, db: AsyncSession, *, obj_in: RecipeCreate) -> Recipe:
        db_obj = Recipe(**obj_in.__dict__)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


recipe_repository = RecipeRepository(Recipe)

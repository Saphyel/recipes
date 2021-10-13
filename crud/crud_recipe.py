from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    async def list(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100, category: Optional[str] = None
    ) -> Iterable[Recipe]:
        query = select(self.model)

        if category:
            query = query.filter(self.model.category_name == category)

        result = await db.execute(query.offset(offset).limit(limit))
        result = await result.scalars()
        return await result.all()

    async def create(self, db: AsyncSession, *, obj_in: RecipeCreate) -> Recipe:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        await db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, title: str) -> Recipe:
        result = await db.execute(select(self.model).filter(Recipe.title == title))
        result = await result.scalars()
        return await result.one()


recipe = CRUDRecipe(Recipe)

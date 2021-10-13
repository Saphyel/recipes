from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.ingredient import Ingredient
from schemas.ingredient import IngredientCreate, IngredientUpdate


class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate, IngredientUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> Iterable[Ingredient]:
        result = await db.execute(select(self.model).offset(offset).limit(limit))
        result = await result.scalars()
        return await result.all()

    async def create(self, db: AsyncSession, *, obj_in: IngredientCreate) -> Ingredient:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        await db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, name: str) -> Ingredient:
        result = await db.execute(select(self.model).filter(Ingredient.name == name))
        result = await result.scalars()
        return await result.one()


ingredient = CRUDIngredient(Ingredient)

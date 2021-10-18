from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.ingredient import Ingredient
from repositories.base import BaseRepository
from schemas.ingredient import IngredientCreate, IngredientUpdate


class IngredientRepository(BaseRepository[Ingredient, IngredientCreate, IngredientUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> List[Ingredient]:
        result = await db.stream_scalars(select(Ingredient).offset(offset).limit(limit))
        return await result.all()

    async def find(self, db: AsyncSession, *, name: str) -> Ingredient:
        result = await db.stream_scalars(select(Ingredient).filter(Ingredient.name == name))
        return await result.one()

    async def create(self, db: AsyncSession, *, obj_in: IngredientCreate) -> Ingredient:
        db_obj = Ingredient(**obj_in.__dict__)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


ingredient_repository = IngredientRepository(Ingredient)

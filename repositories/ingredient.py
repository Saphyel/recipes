from typing import List

from models.ingredient import Ingredient
from schemas.ingredient import IngredientCreate
from sqlalchemy import select, insert
from .base import BaseRepository


class IngredientRepository(BaseRepository):
    async def list(self, *, offset: int = 0, limit: int = 100) -> List[Ingredient]:
        query = select(Ingredient).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def find(self, *, name: str) -> Ingredient:
        query = select(Ingredient).where(Ingredient.name == name)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, *, obj_in: IngredientCreate) -> str:
        query = insert(Ingredient).values(**obj_in.__dict__).returning(Ingredient.name)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def remove(self, *, ingredient: Ingredient) -> None:
        await self.db.delete(ingredient)
        await self.db.commit()

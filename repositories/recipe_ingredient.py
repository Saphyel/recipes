from typing import List

from .base import BaseRepository
from sqlalchemy import select, insert, delete

from models.recipe_ingredient import RecipeIngredient
from schemas.recipe_ingredient import RecipeIngredientCreate


class RecipeIngredientRepository(BaseRepository):
    async def list(self, *, recipe_title: str, offset: int = 0, limit: int = 100) -> List[RecipeIngredient]:
        query = (
            select(RecipeIngredient).where(RecipeIngredient.recipe_title == recipe_title).offset(offset).limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def find(self, *, recipe_title: str, ingredient_name: str) -> RecipeIngredient:
        query = (
            select(RecipeIngredient)
            .where(RecipeIngredient.ingredient_name == ingredient_name)
            .where(RecipeIngredient.recipe_title == recipe_title)
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, *, obj_in: RecipeIngredientCreate, recipe_title: str) -> str:
        query = (
            insert(RecipeIngredient)
            .values(**obj_in.__dict__, recipe_title=recipe_title)
            .returning(RecipeIngredient.recipe_title)
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def remove(self, *, ingredient_name: str, recipe_title: str) -> None:
        query = (
            delete(RecipeIngredient)
            .where(RecipeIngredient.ingredient_name == ingredient_name)
            .where(RecipeIngredient.recipe_title == recipe_title)
            .returning(RecipeIngredient.ingredient_name)
        )
        await self.db.execute(query)

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recipe_ingredient import RecipeIngredient
from repositories.base import BaseRepository
from schemas.recipe_ingredient import RecipeIngredientCreate, RecipeIngredientUpdate


class RecipeIngredientRepository(BaseRepository[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate]):
    async def list(
        self, db: AsyncSession, *, recipe_title: str, offset: int = 0, limit: int = 100
    ) -> List[RecipeIngredient]:
        result = await db.stream_scalars(
            select(RecipeIngredient).filter(RecipeIngredient.recipe_title == recipe_title).offset(offset).limit(limit)
        )
        return await result.all()

    async def find(self, db: AsyncSession, *, recipe_title: str, ingredient_name: str) -> RecipeIngredient:
        result = await (
            db.stream_scalars(
                select(RecipeIngredient)
                .filter(RecipeIngredient.ingredient_name == ingredient_name)
                .filter(RecipeIngredient.recipe_title == recipe_title)
            )
        )
        return await result.one()

    async def create(self, db: AsyncSession, *, obj_in: RecipeIngredientCreate, recipe_title: str) -> RecipeIngredient:
        db_obj = RecipeIngredient(**obj_in.__dict__)
        db_obj.recipe_title = recipe_title
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


recipe_ingredient_repository = RecipeIngredientRepository(RecipeIngredient)

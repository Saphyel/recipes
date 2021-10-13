from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.recipe_ingredient import RecipeIngredient
from schemas.recipe_ingredient import RecipeIngredientCreate, RecipeIngredientUpdate


class CRUDRecipeIngredient(CRUDBase[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate]):
    async def list(
        self, db: Session, *, recipe_title: str, offset: int = 0, limit: int = 100
    ) -> Iterable[RecipeIngredient]:
        result = await db.execute(
            select(self.model).filter(RecipeIngredient.recipe_title == recipe_title).offset(offset).limit(limit)
        )
        result = await result.scalars()
        return await result.all()

    async def create(self, db: AsyncSession, *, obj_in: RecipeIngredientCreate, recipe_title: str) -> RecipeIngredient:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db_obj.recipe_title = recipe_title
        await db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, recipe_title: str, ingredient_name: str) -> RecipeIngredient:
        result = await (
            db.execute(
                select(self.model)
                .filter(RecipeIngredient.ingredient_name == ingredient_name)
                .filter(RecipeIngredient.recipe_title == recipe_title)
            )
        )
        result = await result.scalars()
        return await result.one()


recipe_ingredient = CRUDRecipeIngredient(RecipeIngredient)

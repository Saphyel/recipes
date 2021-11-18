from typing import List

from databases import Database
from sqlalchemy import select, insert, delete

from models.recipe_ingredient import RecipeIngredient
from schemas.recipe_ingredient import RecipeIngredientCreate


class RecipeIngredientRepository:
    async def list(
        self, db: Database, *, recipe_title: str, offset: int = 0, limit: int = 100
    ) -> List[RecipeIngredient]:
        query = (
            select(RecipeIngredient).where(RecipeIngredient.recipe_title == recipe_title).offset(offset).limit(limit)
        )
        result = await db.fetch_all(query)
        return [RecipeIngredient(**item) for item in result]

    async def find(self, db: Database, *, recipe_title: str, ingredient_name: str) -> RecipeIngredient:
        query = (
            select(RecipeIngredient)
            .where(RecipeIngredient.ingredient_name == ingredient_name)
            .where(RecipeIngredient.recipe_title == recipe_title)
        )
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return RecipeIngredient(**result)

    async def create(self, db: Database, *, obj_in: RecipeIngredientCreate, recipe_title: str) -> str:
        query = (
            insert(RecipeIngredient)
            .values(**obj_in.__dict__, recipe_title=recipe_title)
            .returning(RecipeIngredient.recipe_title)
        )
        result = await db.execute(query)
        return result

    async def remove(self, db: Database, *, ingredient_name: str, recipe_title: str) -> None:
        query = (
            delete(RecipeIngredient)
            .where(RecipeIngredient.ingredient_name == ingredient_name)
            .where(RecipeIngredient.recipe_title == recipe_title)
            .returning(RecipeIngredient.ingredient_name)
        )
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")


recipe_ingredient_repository = RecipeIngredientRepository()

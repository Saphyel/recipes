from typing import List

from databases import Database
from sqlalchemy import select, insert, delete

from models.ingredient import Ingredient
from schemas.ingredient import IngredientCreate


class IngredientRepository:
    async def list(self, db: Database, *, offset: int = 0, limit: int = 100) -> List[Ingredient]:
        query = select(Ingredient).offset(offset).limit(limit)
        result = await db.fetch_all(query)
        return [Ingredient(**item) for item in result]  # type: ignore

    async def find(self, db: Database, *, name: str) -> Ingredient:
        query = select(Ingredient).where(Ingredient.name == name)
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return Ingredient(**result)  # type: ignore

    async def create(self, db: Database, *, obj_in: IngredientCreate) -> str:
        query = insert(Ingredient).values(**obj_in.__dict__).returning(Ingredient.name)
        result = await db.execute(query)
        return result

    async def remove(self, db: Database, *, name: str) -> None:
        query = delete(Ingredient).where(Ingredient.name == name).returning(Ingredient.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")

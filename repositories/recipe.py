from typing import Optional, List

from databases import Database
from sqlalchemy import select, insert, delete, update

from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


class RecipeRepository:
    async def list(
        self, db: Database, *, offset: int = 0, limit: int = 100, category: Optional[str] = None
    ) -> List[Recipe]:
        query = select(Recipe)

        if category:
            query = query.where(Recipe.category_name == category)

        query = query.offset(offset).limit(limit)
        result = await db.fetch_all(query)
        return [Recipe(**item) for item in result]  # type: ignore

    async def find(self, db: Database, *, title: str) -> Recipe:
        query = select(Recipe).where(Recipe.title == title)
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return Recipe(**result)  # type: ignore

    async def create(self, db: Database, *, obj_in: RecipeCreate) -> str:
        query = insert(Recipe).values(**obj_in.__dict__).returning(Recipe.title)
        result = await db.execute(query)
        return result

    async def remove(self, db: Database, *, title: str) -> None:
        query = delete(Recipe).where(Recipe.title == title).returning(Recipe.title)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")

    async def update(self, db: Database, *, title: str, obj_in: RecipeUpdate) -> None:
        query = (
            update(Recipe)
            .where(Recipe.title == title)
            .values(**obj_in.dict(exclude_unset=True))
            .returning(Recipe.title)
        )
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")


recipe_repository = RecipeRepository()

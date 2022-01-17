from typing import List

from databases import Database
from sqlalchemy import select, insert, delete, update

from models.chef import Chef
from schemas import ChefCreate, ChefUpdate


class ChefRepository:
    async def list(self, db: Database, *, offset: int = 0, limit: int = 100) -> List[Chef]:
        query = select(Chef).offset(offset).limit(limit)
        result = await db.fetch_all(query)
        return [Chef(**item) for item in result]  # type: ignore

    async def find(self, db: Database, *, name: str) -> Chef:
        query = select(Chef).where(Chef.name == name)
        result = await db.fetch_one(query)
        if not result:
            raise ValueError("Not found")
        return Chef(**result)  # type: ignore

    async def create(self, db: Database, *, obj_in: ChefCreate) -> str:
        query = insert(Chef).values(**obj_in.__dict__).returning(Chef.name)
        result = await db.execute(query)
        return result

    async def remove(self, db: Database, *, name: str) -> None:
        query = delete(Chef).where(Chef.name == name).returning(Chef.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")

    async def update(self, db: Database, *, name: str, obj_in: ChefUpdate) -> None:
        query = update(Chef).where(Chef.name == name).values(**obj_in.dict(exclude_unset=True)).returning(Chef.name)
        result = await db.execute(query)
        if not result:
            raise ValueError("Not found")


chef_repository = ChefRepository()

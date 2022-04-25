from typing import List

from models.chef import Chef
from schemas import ChefCreate, ChefUpdate
from sqlalchemy import select, insert, update
from .base import BaseRepository


class ChefRepository(BaseRepository):
    async def list(self, *, offset: int = 0, limit: int = 100) -> List[Chef]:
        query = select(Chef).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def find(self, *, name: str) -> Chef:
        query = select(Chef).where(Chef.name == name)
        result = await self.db.execute(query)
        return result.unique().scalar_one()

    async def create(self, *, obj_in: ChefCreate) -> str:
        query = insert(Chef).values(**obj_in.__dict__).returning(Chef.name)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def remove(self, *, chef: Chef) -> None:
        await self.db.delete(chef)
        await self.db.commit()

    async def update(self, *, name: str, obj_in: ChefUpdate) -> None:
        query = update(Chef).where(Chef.name == name).values(**obj_in.dict(exclude_unset=True)).returning(Chef.name)
        await self.db.execute(query)

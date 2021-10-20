from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.chef import Chef
from repositories.base import BaseRepository
from schemas import ChefCreate, ChefUpdate


class ChefRepository(BaseRepository[Chef, ChefCreate, ChefUpdate]):
    async def list(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> List[Chef]:
        result = await db.stream_scalars(select(Chef).offset(offset).limit(limit))
        return await result.all()

    async def find(self, db: AsyncSession, *, name: str) -> Chef:
        result = await db.stream_scalars(select(Chef).filter(Chef.name == name))
        return await result.one()

    async def create(self, db: AsyncSession, *, obj_in: ChefCreate) -> Chef:
        db_obj = Chef(**obj_in.__dict__)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


chef_repository = ChefRepository(Chef)

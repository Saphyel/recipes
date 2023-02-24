from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from core.config import settings


@lru_cache(maxsize=None)
def get_engine() -> AsyncEngine:
    return create_async_engine(settings.DATABASE_URL)


async_session = sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()

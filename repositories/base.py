import abc

from db.session import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(metaclass=abc.ABCMeta):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

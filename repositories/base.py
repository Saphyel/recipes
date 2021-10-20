from typing import Generic, Type, TypeVar, NoReturn

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> None:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        await db.commit()
        await db.refresh(db_obj)

    async def remove(self, db: AsyncSession, *, model: ModelType) -> NoReturn:
        await db.delete(model)
        await db.commit()

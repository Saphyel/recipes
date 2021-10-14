from typing import List

from fastapi import APIRouter, Depends, HTTPException

# from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import crud
import schemas
from db.session import get_db
from schemas import Category

router = APIRouter()


@router.get("/", response_model=List[Category])
async def index(db: AsyncSession = Depends(get_db)):
    return [Category(**category.__dict__).dict() for category in await crud.category.list(db=db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create(obj_in: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    try:
        category = await crud.category.create(db=db, obj_in=obj_in)
        return Category(**category.__dict__).dict()
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(400, detail="Resource already exist")
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{name}", response_model=Category)
async def read(name: str, db: AsyncSession = Depends(get_db)):
    try:
        category = await crud.category.get(db=db, name=name)
        return Category(**category.__dict__).dict()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(name: str, db: AsyncSession = Depends(get_db)):
    try:
        await crud.category.remove(db=db, model=await crud.category.get(db=db, name=name))
        return {}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")

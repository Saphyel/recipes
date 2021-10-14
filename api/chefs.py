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
from schemas import Chef

router = APIRouter()


@router.get("/", response_model=List[Chef])
async def index(db: AsyncSession = Depends(get_db)):
    return [Chef(**chef.__dict__).dict() for chef in await crud.chef.list(db=db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Chef)
async def create(obj_in: schemas.ChefCreate, db: AsyncSession = Depends(get_db)):
    try:
        chef = await crud.chef.create(db=db, obj_in=obj_in)
        return Chef(**chef.__dict__).dict()
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(400, detail="Resource already exist")
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{name}", response_model=Chef)
async def read(name: str, db: AsyncSession = Depends(get_db)):
    try:
        chef = await crud.chef.get(db=db, name=name)
        return Chef(**chef.__dict__).dict()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.patch("/{name}", response_model=Chef)
async def update(name: str, obj_in: schemas.ChefUpdate, db: AsyncSession = Depends(get_db)):
    try:
        chef = await crud.chef.get(db=db, name=name)
        await crud.chef.update(db=db, db_obj=chef, obj_in=obj_in)
        return Chef(**chef.__dict__).dict()
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
        pass
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(name: str, db: AsyncSession = Depends(get_db)):
    try:
        await crud.chef.remove(db=db, model=await crud.chef.get(db=db, name=name))
        return {}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")

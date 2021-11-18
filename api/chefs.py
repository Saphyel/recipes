from typing import List

from fastapi import APIRouter, HTTPException

# from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

import schemas
from db.session import database
from models.chef import Chef
from repositories.chef import chef_repository

router = APIRouter()


@router.get("", response_model=List[schemas.Chef])
async def index() -> List[Chef]:
    return await chef_repository.list(db=database)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Chef)
async def create(obj_in: schemas.ChefCreate) -> Chef:
    try:
        result = await chef_repository.create(db=database, obj_in=obj_in)
        return await chef_repository.find(db=database, name=result)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{name}", response_model=schemas.Chef)
async def read(name: str) -> Chef:
    try:
        return await chef_repository.find(db=database, name=name)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.patch("/{name}", response_model=schemas.Chef)
async def update(name: str, obj_in: schemas.ChefUpdate) -> Chef:
    try:
        await chef_repository.update(db=database, name=name, obj_in=obj_in)
        return await chef_repository.find(db=database, name=name)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(name: str) -> str:
    try:
        await chef_repository.remove(db=database, name=name)
        return ""
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

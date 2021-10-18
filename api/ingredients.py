from typing import List

from fastapi import APIRouter, Depends, HTTPException

# from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import schemas
from core.security import get_current_user
from db.session import get_db
from models.ingredient import Ingredient
from repositories.ingredient import ingredient_repository

router = APIRouter()


@router.get("", response_model=List[schemas.Ingredient])
async def index(db: AsyncSession = Depends(get_db)) -> List[Ingredient]:
    return await ingredient_repository.list(db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Ingredient)
async def create(
    obj_in: schemas.IngredientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Ingredient:
    try:
        return await ingredient_repository.create(db=db, obj_in=obj_in)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{name}", response_model=schemas.Ingredient)
async def read(name: str, db: AsyncSession = Depends(get_db)) -> Ingredient:
    try:
        return await ingredient_repository.find(db=db, name=name)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(
    name: str, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> str:
    try:
        await ingredient_repository.remove(db=db, model=await ingredient_repository.find(db=db, name=name))
        return ""
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

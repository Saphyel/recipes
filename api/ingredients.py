from typing import List

from fastapi import APIRouter, HTTPException, Depends

# from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

import schemas
from db.session import database
from models.ingredient import Ingredient
from repositories.ingredient import IngredientRepository

router = APIRouter()


@router.get("", response_model=List[schemas.Ingredient])
async def index(repository: IngredientRepository = Depends(IngredientRepository)) -> List[Ingredient]:
    return await repository.list(db=database)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Ingredient)
async def create(
    obj_in: schemas.IngredientCreate, repository: IngredientRepository = Depends(IngredientRepository)
) -> Ingredient:
    try:
        result = await repository.create(db=database, obj_in=obj_in)
        return await repository.find(db=database, name=result)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{name}", response_model=schemas.Ingredient)
async def read(name: str, repository: IngredientRepository = Depends(IngredientRepository)) -> Ingredient:
    try:
        return await repository.find(db=database, name=name)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(name: str, repository: IngredientRepository = Depends(IngredientRepository)) -> str:
    try:
        await repository.remove(db=database, name=name)
        return ""
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

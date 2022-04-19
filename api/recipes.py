from typing import List

from fastapi import APIRouter, HTTPException, Depends

# from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

import schemas
from db.session import database
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository

router = APIRouter()


@router.get("", response_model=List[schemas.Recipe])
async def index(repository: RecipeRepository = Depends(RecipeRepository)) -> List[Recipe]:
    return await repository.list(db=database)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Recipe,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(obj_in: schemas.RecipeCreate, repository: RecipeRepository = Depends(RecipeRepository)) -> Recipe:
    try:
        result = await repository.create(db=database, obj_in=obj_in)
        return await repository.find(db=database, title=result)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Foreign resources not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get(
    "/{title}",
    response_model=schemas.Recipe,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> Recipe:
    try:
        return await repository.find(db=database, title=title)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.patch(
    "/{title}",
    response_model=schemas.Recipe,
    responses={
        400: {"description": "Invalid request", "model": schemas.HttpError},
        404: {"description": "Resource not found", "model": schemas.HttpError},
    },
)
async def update(
    title: str, obj_in: schemas.RecipeUpdate, repository: RecipeRepository = Depends(RecipeRepository)
) -> Recipe:
    try:
        await repository.update(db=database, title=title, obj_in=obj_in)
        return await repository.find(db=database, title=title)
    except ValidationError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except IntegrityError as error:
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Foreign resources not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    "/{title}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> str:
    try:
        await repository.remove(db=database, title=title)
        return ""
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.get("/{title}/ingredients", response_model=List[schemas.RecipeIngredient])
async def ingredients_index(
    title: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> List[RecipeIngredient]:
    return await repository.list(db=database, recipe_title=title)


@router.delete(
    "/{title}/ingredients/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def ingredients_remove(
    title: str, name: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> str:
    try:
        await repository.remove(db=database, recipe_title=title, ingredient_name=name)
        return ""
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

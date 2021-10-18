from typing import List

from fastapi import APIRouter, Depends, HTTPException

# from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import schemas
from core.security import get_current_user
from db.session import get_db
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from repositories.recipe import recipe_repository
from repositories.recipe_ingredient import recipe_ingredient_repository

router = APIRouter()


@router.get("", response_model=List[schemas.Recipe])
async def index(db: AsyncSession = Depends(get_db)) -> List[Recipe]:
    return await recipe_repository.list(db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Recipe)
async def create(
    obj_in: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Recipe:
    try:
        return await recipe_repository.create(db=db, obj_in=obj_in)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Foreign resources not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{title}", response_model=Recipe)
async def read(title: str, db: AsyncSession = Depends(get_db)) -> Recipe:
    try:
        return await recipe_repository.find(db=db, title=title)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.patch("/{title}", response_model=schemas.Recipe)
async def update(
    title: str,
    obj_in: schemas.RecipeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Recipe:
    try:
        recipe = await recipe_repository.find(db=db, title=title)
        return await recipe_repository.update(db=db, db_obj=recipe, obj_in=obj_in)
    except ValidationError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except IntegrityError as error:
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Foreign resources not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{title}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(
    title: str, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> str:
    try:
        await recipe_repository.remove(db=db, model=await recipe_repository.find(db=db, title=title))
        return ""
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.get("/{title}/ingredients", response_model=List[schemas.RecipeIngredient])
async def ingredients_index(title: str, db: AsyncSession = Depends(get_db)) -> List[RecipeIngredient]:
    return await recipe_ingredient_repository.list(db=db, recipe_title=title)


@router.delete("/{title}/ingredients/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def ingredients_remove(
    title: str, name: str, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
) -> str:
    try:
        await recipe_ingredient_repository.remove(
            db=db, model=await recipe_ingredient_repository.find(db=db, recipe_title=title, ingredient_name=name)
        )
        return ""
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

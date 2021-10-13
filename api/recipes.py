from typing import List

from fastapi import APIRouter, Depends, HTTPException

# from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import crud
import schemas
from db.session import get_db
from schemas import Recipe, RecipeIngredient

router = APIRouter()


@router.get("/", response_model=List[Recipe])
async def index(db: AsyncSession = Depends(get_db)):
    return [Recipe(**recipe.__dict__).dict() for recipe in await crud.recipe.list(db=db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Recipe)
async def create(obj_in: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    try:
        recipe = await crud.recipe.create(db=db, obj_in=obj_in)
        return Recipe(**recipe.__dict__).dict()
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(400, detail="Resource already exist")
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(400, detail="Foreign resources not found")
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{title}", response_model=Recipe)
async def read(title: str, db: AsyncSession = Depends(get_db)):
    try:
        recipe = await crud.recipe.get(db=db, title=title)
        return Recipe(**recipe.__dict__).dict()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.patch("/{title}", response_model=Recipe)
async def update(title: str, obj_in: schemas.RecipeUpdate, db: AsyncSession = Depends(get_db)):
    try:
        recipe = await crud.recipe.get(db=db, title=title)
        await crud.recipe.update(db=db, db_obj=recipe, obj_in=obj_in)
        return Recipe(**recipe.__dict__).dict()
    except ValidationError as error:
        raise HTTPException(400, detail=str(error))
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")
    except IntegrityError as error:
        # if error.orig == ForeignKeyViolation:
        #     raise HTTPException(400, detail="Foreign resources not found")
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/{title}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(title: str, db: AsyncSession = Depends(get_db)):
    try:
        await crud.recipe.remove(db=db, model=await crud.recipe.get(db=db, title=title))
        return {}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.get("/{title}/ingredients", response_model=List[RecipeIngredient])
async def ingredients_index(title: str, db: AsyncSession = Depends(get_db)):
    return [
        RecipeIngredient(**ingredient.__dict__).dict()
        for ingredient in await crud.recipe_ingredient.list(db=db, recipe_title=title)
    ]


@router.delete("/{title}/ingredients/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def ingredients_remove(title: str, name: str, db: AsyncSession = Depends(get_db)):
    try:
        await crud.recipe_ingredient.remove(
            db=db, model=await crud.recipe_ingredient.get(db=db, recipe_title=title, ingredient_name=name)
        )
        return {}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resource not found")

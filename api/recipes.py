import logging
from typing import List

import schemas
from fastapi import APIRouter, Depends, HTTPException
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

logger = logging.getLogger(f"recipes.{__name__}")
router = APIRouter()


@router.get("", response_model=List[schemas.Recipe])
async def index(repository: RecipeRepository = Depends(RecipeRepository)) -> List[Recipe]:
    try:
        return await repository.list()
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Recipe,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(obj_in: schemas.RecipeCreate, repository: RecipeRepository = Depends(RecipeRepository)) -> Recipe:
    try:
        result = await repository.create(obj_in=obj_in)
        return await repository.find(title=result)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.get(
    "/{title}",
    response_model=schemas.Recipe,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> Recipe:
    try:
        return await repository.find(title=title)
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


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
        await repository.update(title=title, obj_in=obj_in)
        return await repository.find(title=title)
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.delete(
    "/{title}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> None:
    try:
        await repository.remove(recipe=await repository.find(title=title))
        return None
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.get("/{title}/ingredients", response_model=List[schemas.RecipeIngredient])
async def ingredients_index(
    title: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> List[RecipeIngredient]:
    try:
        return await repository.list(recipe_title=title)
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.delete(
    "/{title}/ingredients/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def ingredients_remove(
    title: str, name: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> None:
    try:
        await repository.remove(recipe_title=title, ingredient_name=name)
        return None
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")

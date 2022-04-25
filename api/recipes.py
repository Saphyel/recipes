from typing import List

import schemas
from fastapi import APIRouter, HTTPException, Depends
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

router = APIRouter()


@router.get("", response_model=List[schemas.Recipe])
async def index(repository: RecipeRepository = Depends(RecipeRepository)) -> List[Recipe]:
    try:
        return await repository.list()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


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
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Integrity error")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.get(
    "/{title}",
    response_model=schemas.Recipe,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> Recipe:
    try:
        return await repository.find(title=title)
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


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
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Integrity error")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.delete(
    "/{title}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(title: str, repository: RecipeRepository = Depends(RecipeRepository)) -> str:
    try:
        await repository.remove(recipe=await repository.find(title=title))
        return ""
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.get("/{title}/ingredients", response_model=List[schemas.RecipeIngredient])
async def ingredients_index(
    title: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> List[RecipeIngredient]:
    try:
        return await repository.list(recipe_title=title)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.delete(
    "/{title}/ingredients/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def ingredients_remove(
    title: str, name: str, repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository)
) -> str:
    try:
        await repository.remove(recipe_title=title, ingredient_name=name)
        return ""
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")

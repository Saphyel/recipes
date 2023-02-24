import logging
from typing import List

import schemas
from fastapi import APIRouter, Depends, HTTPException
from models.category import Category
from repositories.category import CategoryRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

logger = logging.getLogger(f"recipes.{__name__}")

router = APIRouter()


@router.get("", response_model=List[schemas.Category])
async def index(repository: CategoryRepository = Depends(CategoryRepository)) -> List[Category]:
    try:
        return await repository.list()
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Category,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(
    obj_in: schemas.CategoryCreate, repository: CategoryRepository = Depends(CategoryRepository)
) -> Category:
    try:
        return await repository.create(obj_in=obj_in)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.get(
    "/{name}",
    response_model=schemas.Category,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: CategoryRepository = Depends(CategoryRepository)) -> Category:
    try:
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(name: str, repository: CategoryRepository = Depends(CategoryRepository)) -> None:
    try:
        await repository.remove(category=await repository.find(name=name))
        return None
    except (ValueError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="What have you done??")

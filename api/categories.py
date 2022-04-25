from typing import List

import schemas
from fastapi import APIRouter, HTTPException, Depends
from models.category import Category
from repositories.category import CategoryRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

router = APIRouter()


@router.get("", response_model=List[schemas.Category])
async def index(repository: CategoryRepository = Depends(CategoryRepository)) -> List[Category]:
    try:
        return await repository.list()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


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
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resource already exist")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.get(
    "/{name}",
    response_model=schemas.Category,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: CategoryRepository = Depends(CategoryRepository)) -> Category:
    try:
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(name: str, repository: CategoryRepository = Depends(CategoryRepository)) -> str:
    try:
        await repository.remove(category=await repository.find(name=name))
        return ""
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")

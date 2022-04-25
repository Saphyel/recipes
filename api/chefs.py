from typing import List

import schemas
from fastapi import APIRouter, HTTPException, Depends
from models.chef import Chef
from repositories.chef import ChefRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

router = APIRouter()


@router.get("", response_model=List[schemas.Chef])
async def index(repository: ChefRepository = Depends(ChefRepository)) -> List[Chef]:
    try:
        return await repository.list()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Chef,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(obj_in: schemas.ChefCreate, repository: ChefRepository = Depends(ChefRepository)) -> Chef:
    try:
        result = await repository.create(obj_in=obj_in)
        return await repository.find(name=result)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resource already exist")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.get(
    "/{name}",
    response_model=schemas.Chef,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: ChefRepository = Depends(ChefRepository)) -> Chef:
    try:
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")


@router.patch(
    "/{name}",
    response_model=schemas.Chef,
    responses={
        400: {"description": "Invalid request", "model": schemas.HttpError},
        404: {"description": "Resource not found", "model": schemas.HttpError},
    },
)
async def update(name: str, obj_in: schemas.ChefUpdate, repository: ChefRepository = Depends(ChefRepository)) -> Chef:
    try:
        await repository.update(name=name, obj_in=obj_in)
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
async def remove(name: str, repository: ChefRepository = Depends(ChefRepository)) -> str:
    try:
        await repository.remove(chef=await repository.find(name=name))
        return ""
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")

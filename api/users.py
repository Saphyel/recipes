from typing import List

from fastapi import APIRouter, Depends, HTTPException

# from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

import schemas
from core.security import get_current_user
from db.session import database
from models.user import User
from repositories.user import UserRepository

router = APIRouter()


@router.get("", response_model=List[schemas.User])
async def index(
    current_user: schemas.User = Depends(get_current_user), repository: UserRepository = Depends(UserRepository)
) -> List[User]:
    return await repository.list(db=database)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(
    obj_in: schemas.UserCreate,
    current_user: schemas.User = Depends(get_current_user),
    repository: UserRepository = Depends(UserRepository),
) -> User:
    try:
        result = await repository.create(db=database, obj_in=obj_in)
        return await repository.find(db=database, name=result)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError as error:
        # if error.orig == UniqueViolation:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Resource already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get(
    "/{name}",
    response_model=schemas.User,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: UserRepository = Depends(UserRepository)) -> User:
    try:
        return await repository.find(db=database, name=name)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(
    name: str,
    current_user: schemas.User = Depends(get_current_user),
    repository: UserRepository = Depends(UserRepository),
) -> str:
    try:
        await repository.remove(db=database, name=name)
        return ""
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

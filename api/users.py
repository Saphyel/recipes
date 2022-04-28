from typing import List, Union

import schemas
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.user import User
from repositories.user import UserRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

# from core.security import get_current_user

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.User],
    responses={401: {"description": "Unauthorized", "model": schemas.HttpError}},
)
async def index(
    # current_user: schemas.User = Depends(get_current_user),
    repository: UserRepository = Depends(UserRepository),
) -> Union[List[User], JSONResponse]:
    try:
        return await repository.list()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
    responses={
        400: {"description": "Invalid request", "model": schemas.HttpError},
        401: {"description": "Unauthorized", "model": schemas.HttpError},
    },
)
async def create(
    obj_in: schemas.UserCreate,
    # current_user: schemas.User = Depends(get_current_user),
    repository: UserRepository = Depends(UserRepository),
) -> Union[User, JSONResponse]:
    try:
        result = await repository.create(obj_in=obj_in)
        return await repository.find(name=result)
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(schemas.HttpError(detail="Resource already exist")),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.get(
    "/{name}",
    response_model=schemas.User,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: UserRepository = Depends(UserRepository)) -> Union[User, JSONResponse]:
    try:
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(schemas.HttpError(detail="Resource not found")),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Unauthorized", "model": schemas.HttpError},
        404: {"description": "Resource not found", "model": schemas.HttpError},
    },
)
async def remove(
    name: str,
    # current_user: schemas.User = Depends(get_current_user),
    repository: UserRepository = Depends(UserRepository),
) -> Union[None, JSONResponse]:
    try:
        await repository.remove(user=await repository.find(name=name))
        return ""
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(schemas.HttpError(detail="Resource not found")),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )

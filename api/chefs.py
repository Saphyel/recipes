import logging
from typing import List, Union

import schemas
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.chef import Chef
from repositories.chef import ChefRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

logger = logging.getLogger(f"recipes.{__name__}")

router = APIRouter()


@router.get("", response_model=List[schemas.Chef])
async def index(repository: ChefRepository = Depends(ChefRepository)) -> Union[List[Chef], JSONResponse]:
    try:
        return await repository.list()
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Chef,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(
    obj_in: schemas.ChefCreate, repository: ChefRepository = Depends(ChefRepository)
) -> Union[Chef, JSONResponse]:
    try:
        result = await repository.create(obj_in=obj_in)
        return await repository.find(name=result)
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(schemas.HttpError(detail="Resource already exist")),
        )
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.get(
    "/{name}",
    response_model=schemas.Chef,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(name: str, repository: ChefRepository = Depends(ChefRepository)) -> Union[Chef, JSONResponse]:
    try:
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(schemas.HttpError(detail="Resource not found")),
        )
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.patch(
    "/{name}",
    response_model=schemas.Chef,
    responses={
        400: {"description": "Invalid request", "model": schemas.HttpError},
        404: {"description": "Resource not found", "model": schemas.HttpError},
    },
)
async def update(
    name: str, obj_in: schemas.ChefUpdate, repository: ChefRepository = Depends(ChefRepository)
) -> Union[Chef, JSONResponse]:
    try:
        await repository.update(name=name, obj_in=obj_in)
        return await repository.find(name=name)
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(schemas.HttpError(detail="Resource not found")),
        )
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(name: str, repository: ChefRepository = Depends(ChefRepository)) -> Union[None, JSONResponse]:
    try:
        await repository.remove(chef=await repository.find(name=name))
        return None
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(schemas.HttpError(detail="Resource not found")),
        )
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(schemas.HttpError(detail="What have you done??")),
        )

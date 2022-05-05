import logging
from typing import List, Union

import schemas
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.category import Category
from repositories.category import CategoryRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

logger = logging.getLogger(f"recipes.{__name__}")

router = APIRouter()


@router.get("", response_model=List[schemas.Category])
async def index(repository: CategoryRepository = Depends(CategoryRepository)) -> Union[List[Category], JSONResponse]:
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
    response_model=schemas.Category,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(
    obj_in: schemas.CategoryCreate, repository: CategoryRepository = Depends(CategoryRepository)
) -> Union[Category, JSONResponse]:
    try:
        return await repository.create(obj_in=obj_in)
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
    response_model=schemas.Category,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(
    name: str, repository: CategoryRepository = Depends(CategoryRepository)
) -> Union[Category, JSONResponse]:
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


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(name: str, repository: CategoryRepository = Depends(CategoryRepository)) -> Union[None, JSONResponse]:
    try:
        await repository.remove(category=await repository.find(name=name))
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

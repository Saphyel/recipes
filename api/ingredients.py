from typing import List, Union

import schemas
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.ingredient import Ingredient
from repositories.ingredient import IngredientRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

router = APIRouter()


@router.get("", response_model=List[schemas.Ingredient])
async def index(
    repository: IngredientRepository = Depends(IngredientRepository),
) -> Union[List[Ingredient], JSONResponse]:
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
    response_model=schemas.Ingredient,
    responses={400: {"description": "Invalid request", "model": schemas.HttpError}},
)
async def create(
    obj_in: schemas.IngredientCreate, repository: IngredientRepository = Depends(IngredientRepository)
) -> Union[Ingredient, JSONResponse]:
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
    response_model=schemas.Ingredient,
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def read(
    name: str, repository: IngredientRepository = Depends(IngredientRepository)
) -> Union[Ingredient, JSONResponse]:
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
    responses={404: {"description": "Resource not found", "model": schemas.HttpError}},
)
async def remove(
    name: str, repository: IngredientRepository = Depends(IngredientRepository)
) -> Union[None, JSONResponse]:
    try:
        await repository.remove(ingredient=await repository.find(name=name))
        return None
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

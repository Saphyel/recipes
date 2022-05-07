import logging

from core import security
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from repositories.user import UserRepository
from schemas import Token, HttpError
from sqlalchemy.exc import NoResultFound
from starlette import status

logger = logging.getLogger(f"recipes.{__name__}")
router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    responses={400: {"description": "Invalid request", "model": HttpError}},
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), user=None, repository: UserRepository = Depends(UserRepository)
) -> dict | JSONResponse:
    try:
        user = await repository.find(name=form_data.username)
        if not await repository.authenticate(db_obj=user, password=form_data.password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(HttpError(detail="Incorrect name or password")),
            )
        return {"access_token": security.create_access_token(user.name), "token_type": "bearer"}
    except (ValueError, NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(HttpError(detail="Incorrect name or password")),
        )
    except Exception as error:
        logger.error("Server error", extra={"error": error})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(HttpError(detail="What have you done??")),
        )

from core import security
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from repositories.user import UserRepository
from schemas import Token, HttpError
from sqlalchemy.exc import NoResultFound
from starlette import status

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    responses={400: {"description": "Invalid request", "model": HttpError}},
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), user=None, repository: UserRepository = Depends(UserRepository)
) -> dict:
    try:
        user = await repository.find(name=form_data.username)
        if not await repository.authenticate(db_obj=user, password=form_data.password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect name or password")
        return {"access_token": security.create_access_token(user.name), "token_type": "bearer"}
    except (ValueError, NoResultFound):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect name or password")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")

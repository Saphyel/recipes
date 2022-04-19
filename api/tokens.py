from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core import security
from db.session import database
from repositories.user import UserRepository
from schemas import Token, HttpError

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
        user = await repository.find(db=database, name=form_data.username)
        if not await repository.authenticate(db_obj=user, password=form_data.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect name or password")
        return {"access_token": security.create_access_token(user.name), "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect name or password")

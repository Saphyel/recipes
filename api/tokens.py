from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.exc import NoResultFound

from core import security
from db.session import get_db
from repositories.user import user_repository
from schemas import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), user=None
) -> dict:
    try:
        user = await user_repository.find(db, name=form_data.username)
        if not await user_repository.authenticate(db_obj=user, password=form_data.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect name or password")
        return {"access_token": security.create_access_token(user.name), "token_type": "bearer"}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect name or password")

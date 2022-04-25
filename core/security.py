from datetime import timedelta, datetime
from typing import Optional

from core.config import settings, reusable_oauth2
from fastapi import Depends, HTTPException
from jose import jwt
from models.user import User
from repositories.user import UserRepository
from schemas import TokenPayload
from sqlalchemy.exc import NoResultFound
from starlette import status


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "name": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(reusable_oauth2), repository: UserRepository = Depends(UserRepository)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        user = await repository.find(name=token_data.name)
        return user
    except (jwt.JWTError, NoResultFound):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "What have you done??")

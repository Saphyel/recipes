import os
import secrets
from pathlib import Path
from typing import Final

from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=f"{BASE_PATH}/templates/")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")


class Settings:
    PROJECT_NAME: Final = os.environ.get("PROJECT_NAME", "Fantasy Recipes")
    SECRET_KEY: Final = secrets.token_urlsafe(32)
    DATABASE_URL: Final = (
        os.environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://", 1).replace("://", "+asyncpg://", 1)
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: Final = 60 * 24 * 8

    ALGORITHM: Final = "HS256"


settings = Settings()

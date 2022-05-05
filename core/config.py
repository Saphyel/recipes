import os
import secrets
from logging.config import dictConfig
from pathlib import Path
from typing import Final

from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=f"{BASE_PATH}/templates/")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "recipes": {"handlers": ["default"], "level": "DEBUG"},
    },
}

dictConfig(log_config)


class Settings:
    PROJECT_NAME: Final = os.environ.get("PROJECT_NAME", "Fantasy Recipes")
    SECRET_KEY: Final = secrets.token_urlsafe(32)
    DATABASE_URL: Final = (
        os.environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://", 1).replace("://", "+asyncpg://", 1)
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: Final = 60 * 24 * 8

    ALGORITHM: Final = "HS256"


settings = Settings()

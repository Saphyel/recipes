import os
from pathlib import Path
from typing import Final

from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=f"{BASE_PATH}/templates/")


class Settings:
    PROJECT_NAME: Final = os.environ.get("PROJECT_NAME", "Fantasy Recipes")
    DATABASE_URL: Final = (
        os.environ["DATABASE_URL"].replace("postgres://", "postgresql://", 1).replace("://", "+asyncpg://", 1)
    )


settings = Settings()

import os


class Settings:
    DATABASE_URL: str = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://", 1)


settings = Settings()

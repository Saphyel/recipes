from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

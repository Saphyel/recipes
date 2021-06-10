from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.user import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[User]:
        return db.query(self.model).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, name: str) -> User:
        return db.query(self.model).filter(User.name == name).one()


user = CRUDUser(User)

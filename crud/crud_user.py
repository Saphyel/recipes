from typing import Optional, Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.user import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[User]:
        return db.query(self.model).offset(offset).limit(limit)

    def get(self, db: Session, *, name: str) -> Optional[User]:
        return db.query(self.model).filter(User.name == name).one()


user = CRUDUser(User)

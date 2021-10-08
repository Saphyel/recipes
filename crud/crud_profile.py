from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.profile import Profile
from schemas import ProfileCreate, ProfileUpdate


class CRUDProfile(CRUDBase[Profile, ProfileCreate, ProfileUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[Profile]:
        return db.query(self.model).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: ProfileCreate) -> Profile:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, name: str) -> Profile:
        return db.query(self.model).filter(Profile.name == name).one()


profile = CRUDProfile(Profile)

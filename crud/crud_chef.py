from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.chef import Chef
from schemas import ChefCreate, ChefUpdate


class CRUDChef(CRUDBase[Chef, ChefCreate, ChefUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[Chef]:
        return db.query(self.model).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: ChefCreate) -> Chef:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, name: str) -> Chef:
        return db.query(self.model).filter(Chef.name == name).one()


chef = CRUDChef(Chef)

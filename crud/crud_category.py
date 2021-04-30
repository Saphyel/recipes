from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[Category]:
        return db.query(self.model).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, name: str) -> Category:
        return db.query(self.model).filter(Category.name == name).one()


category = CRUDCategory(Category)

from typing import Optional, Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[Category]:
        return db.query(self.model).offset(offset).limit(limit)

    def get(self, db: Session, *, name: str) -> Optional[Category]:
        return db.query(self.model).filter(Category.name == name).one()


category = CRUDCategory(Category)

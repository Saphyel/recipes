from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.ingredient import Ingredient
from schemas.ingredient import IngredientCreate, IngredientUpdate


class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate, IngredientUpdate]):
    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> Iterable[Ingredient]:
        return db.query(self.model).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: IngredientCreate) -> Ingredient:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, name: str) -> Ingredient:
        return db.query(self.model).filter(Ingredient.name == name).one()


ingredient = CRUDIngredient(Ingredient)

from typing import Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.recipe_ingredient import RecipeIngredient
from schemas.recipe_ingredient import RecipeIngredientCreate, RecipeIngredientUpdate


class CRUDRecipeIngredient(CRUDBase[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate]):
    def list(self, db: Session, *, recipe_title: str, offset: int = 0, limit: int = 100) -> Iterable[RecipeIngredient]:
        return db.query(self.model).filter(RecipeIngredient.recipe_title == recipe_title).offset(offset).limit(limit)

    def create(self, db: Session, *, obj_in: RecipeIngredientCreate, recipe_title: str) -> RecipeIngredient:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db_obj.recipe_title = recipe_title
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, recipe_title: str, ingredient_name: str) -> RecipeIngredient:
        return db.query(self.model).filter(RecipeIngredient.ingredient_name == ingredient_name).filter(
            RecipeIngredient.recipe_title == recipe_title).one()


recipe_ingredient = CRUDRecipeIngredient(RecipeIngredient)

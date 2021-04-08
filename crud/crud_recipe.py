from typing import Optional, Iterable

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.recipe import Recipe
from schemas import RecipeCreate, RecipeUpdate


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    def list(
        self, db: Session, *, offset: int = 0, limit: int = 100, category: Optional[str] = None
    ) -> Iterable[Recipe]:
        query = db.query(self.model)

        if category:
            query = query.filter(self.model.category_name == category)

        return query.offset(offset).limit(limit)

    def get(self, db: Session, *, title: str) -> Recipe:
        return db.query(self.model).filter(Recipe.title == title).one()


recipe = CRUDRecipe(Recipe)

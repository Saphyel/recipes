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

    def create(self, db: Session, *, obj_in: RecipeCreate) -> Recipe:
        db_obj = self.model(**obj_in.__dict__)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, title: str) -> Recipe:
        return db.query(self.model).filter(Recipe.title == title).one()


recipe = CRUDRecipe(Recipe)

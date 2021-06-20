from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base_class import mapper_registry, Base
from models.ingredient import Ingredient
from models.recipe import Recipe


# cuddles and a laugh
@mapper_registry.mapped
@dataclass
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"  # type: ignore
    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    recipe_title: str = field(metadata={"sa": Column(ForeignKey("recipe.title"))})
    ingredient_name: str = field(metadata={"sa": Column(ForeignKey("ingredient.name"))})
    quantity: str = field(metadata={"sa": Column(String)})
    recipe: Recipe = field(metadata={"sa": relationship("Recipe", uselist=False)})
    ingredient: Ingredient = field(metadata={"sa": relationship("Ingredient", uselist=False)})

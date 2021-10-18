from typing import Annotated

from pydantic import BaseModel, Field


class RecipeIngredientInput(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class RecipeIngredientCreate(RecipeIngredientInput):
    ingredient_name: Annotated[str, Field(min_length=3)]


class RecipeIngredientUpdate(RecipeIngredientInput):
    quantity: Annotated[str, Field(min_length=1)]


class RecipeIngredientOutput(RecipeIngredientInput):
    id: int
    quantity: str

    class Config:
        orm_mode = True


class RecipeIngredient(RecipeIngredientOutput):
    ingredient_name: str

from typing import Annotated

from pydantic import BaseModel, Field


class RecipeIngredientBase(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class RecipeIngredientCreate(RecipeIngredientBase):
    ingredient_name: Annotated[str, Field(min_length=3)]


class RecipeIngredientUpdate(RecipeIngredientBase):
    quantity: Annotated[str, Field(min_length=1)]


class RecipeIngredientInDBBase(RecipeIngredientBase):
    id: int
    quantity: str

    class Config:
        orm_mode = True


class RecipeIngredient(RecipeIngredientInDBBase):
    ingredient_name: str

from typing import Annotated

from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    pass

    class Config:
        anystr_strip_whitespace = True


class IngredientCreate(IngredientBase):
    name: Annotated[str, Field(min_length=3)]


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDBBase(IngredientBase):
    name: str

    class Config:
        orm_mode = True


class Ingredient(IngredientInDBBase):
    pass

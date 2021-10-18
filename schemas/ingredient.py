from typing import Annotated

from pydantic import BaseModel, Field


class IngredientInput(BaseModel):
    pass

    class Config:
        anystr_strip_whitespace = True


class IngredientCreate(IngredientInput):
    name: Annotated[str, Field(min_length=3)]


class IngredientUpdate(IngredientInput):
    pass


class IngredientOutput(IngredientInput):
    name: str

    class Config:
        orm_mode = True


class Ingredient(IngredientOutput):
    pass

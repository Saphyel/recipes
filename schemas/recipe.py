from typing import Optional, Annotated

from pydantic import BaseModel, Field, AnyUrl


class RecipeInput(BaseModel):
    image: Annotated[Optional[str], Field(min_length=5)] = None
    active_cook: Annotated[Optional[int], Field(gt=0)] = None
    total_cook: Annotated[Optional[int], Field(gt=0)] = None
    serves: Annotated[Optional[int], Field(gt=0)] = None
    description: Annotated[Optional[str], Field(min_length=9)] = None
    instructions: Annotated[Optional[str], Field(min_length=9)] = None
    url: Annotated[Optional[AnyUrl], Field] = None

    class Config:
        anystr_strip_whitespace = True


class RecipeCreate(RecipeInput):
    title: Annotated[str, Field(min_length=3)]
    category_name: Annotated[Optional[str], Field(min_length=3)] = None
    chef_name: Annotated[Optional[str], Field(min_length=3)] = None


class RecipeUpdate(RecipeInput):
    category_name: Annotated[Optional[str], Field(min_length=3)]
    chef_name: Annotated[Optional[str], Field(min_length=3)]


class RecipeOutput(RecipeInput):
    title: str

    class Config:
        orm_mode = True


class Recipe(RecipeOutput):
    category_name: Optional[str] = None
    chef_name: Optional[str] = None

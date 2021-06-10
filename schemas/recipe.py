from typing import Optional, Annotated

from pydantic import BaseModel, Field, AnyUrl


class RecipeBase(BaseModel):
    image: Annotated[Optional[str], Field(min_length=5)] = None
    active_cook: Annotated[Optional[int], Field(gt=0)] = None
    total_cook: Annotated[Optional[int], Field(gt=0)] = None
    serves: Annotated[Optional[int], Field(gt=0)] = None
    description: Annotated[Optional[str], Field(min_length=9)] = None
    instructions: Annotated[Optional[str], Field(min_length=9)] = None
    url: Annotated[Optional[AnyUrl], Field] = None

    class Config:
        anystr_strip_whitespace = True


class RecipeCreate(RecipeBase):
    title: Annotated[str, Field(min_length=3)]
    category_name: Annotated[Optional[str], Field(min_length=3)] = None
    user_name: Annotated[Optional[str], Field(min_length=3)] = None


class RecipeUpdate(RecipeBase):
    category_name: Annotated[Optional[str], Field(min_length=3)]
    user_name: Annotated[Optional[str], Field(min_length=3)]


class RecipeInDBBase(RecipeBase):
    title: str

    class Config:
        orm_mode = True


class Recipe(RecipeInDBBase):
    category_name: Optional[str] = None
    user_name: Optional[str] = None

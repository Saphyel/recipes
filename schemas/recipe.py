from typing import Optional

from pydantic import BaseModel, PositiveInt, constr, AnyUrl


class RecipeBase(BaseModel):
    image: Optional[constr(min_length=5)] = None
    active_cook: Optional[PositiveInt] = None
    total_cook: Optional[PositiveInt] = None
    serves: Optional[PositiveInt] = None
    description: Optional[constr(min_length=9)] = None
    instructions: Optional[constr(min_length=9)] = None
    url: Optional[AnyUrl] = None


class RecipeCreate(RecipeBase):
    title: constr(min_length=3)
    category_name: Optional[str] = None
    user_name: Optional[str] = None


class RecipeUpdate(RecipeBase):
    category_name: Optional[str] = None
    user_name: Optional[str] = None


class RecipeInDBBase(RecipeBase):
    title: str

    class Config:
        orm_mode = True


class Recipe(RecipeInDBBase):
    category_name: Optional[str] = None
    user_name: Optional[str] = None

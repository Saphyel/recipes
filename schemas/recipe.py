from typing import Optional

from pydantic import BaseModel


class RecipeBase(BaseModel):
    image: Optional[str] = None
    active_cook: Optional[int] = None
    total_cook: Optional[int] = None
    serves: Optional[int] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    url: Optional[str] = None


class RecipeCreate(RecipeBase):
    title: str
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

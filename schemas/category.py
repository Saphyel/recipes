from typing import Annotated

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    pass

    class Config:
        anystr_strip_whitespace = True


class CategoryCreate(CategoryBase):
    name: Annotated[str, Field(min_length=3)]


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    name: str

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass

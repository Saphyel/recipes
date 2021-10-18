from typing import Annotated

from pydantic import BaseModel, Field


class CategoryInput(BaseModel):
    pass

    class Config:
        anystr_strip_whitespace = True


class CategoryCreate(CategoryInput):
    name: Annotated[str, Field(min_length=3)]


class CategoryUpdate(CategoryInput):
    pass


class CategoryOutput(CategoryInput):
    name: str

    class Config:
        orm_mode = True


class Category(CategoryOutput):
    pass

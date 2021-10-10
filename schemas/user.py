from typing import Optional, Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class UserCreate(UserBase):
    name: Annotated[str, Field(min_length=3)]
    password: Annotated[str, Field(min_length=3)]


class UserUpdate(UserBase):
    password: Annotated[str, Field(min_length=3)]


class UserInDBBase(UserBase):
    name: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

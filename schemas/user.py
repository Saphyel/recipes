from typing import Optional, Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    reddit: Annotated[Optional[str], Field(min_length=3)] = None
    instagram: Annotated[Optional[str], Field(min_length=3)] = None
    twitter: Annotated[Optional[str], Field(min_length=3)] = None

    class Config:
        anystr_strip_whitespace = True


class UserCreate(UserBase):
    name: Annotated[str, Field(min_length=3)]


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    name: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

from typing import Annotated

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class UserCreate(UserInput):
    name: Annotated[str, Field(min_length=3)]
    password: Annotated[str, Field(min_length=3)]


class UserUpdate(UserInput):
    password: Annotated[str, Field(min_length=3)]


class UserOutput(UserInput):
    name: str

    class Config:
        orm_mode = True


class User(UserOutput):
    pass

from typing import Optional, Annotated

from pydantic import BaseModel, Field


class ChefInput(BaseModel):
    reddit: Annotated[Optional[str], Field(min_length=3)] = None
    instagram: Annotated[Optional[str], Field(min_length=3)] = None
    twitter: Annotated[Optional[str], Field(min_length=3)] = None

    class Config:
        anystr_strip_whitespace = True


class ChefCreate(ChefInput):
    name: Annotated[str, Field(min_length=3)]


class ChefUpdate(ChefInput):
    pass


class ChefOutput(ChefInput):
    name: str

    class Config:
        orm_mode = True


class Chef(ChefOutput):
    pass

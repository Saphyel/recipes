from typing import Optional, Annotated

from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    reddit: Annotated[Optional[str], Field(min_length=3)] = None
    instagram: Annotated[Optional[str], Field(min_length=3)] = None
    twitter: Annotated[Optional[str], Field(min_length=3)] = None

    class Config:
        anystr_strip_whitespace = True


class ProfileCreate(ProfileBase):
    name: Annotated[str, Field(min_length=3)]


class ProfileUpdate(ProfileBase):
    pass


class ProfileInDBBase(ProfileBase):
    name: str

    class Config:
        orm_mode = True


class Profile(ProfileInDBBase):
    pass

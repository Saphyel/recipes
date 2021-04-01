from typing import Optional

from pydantic import BaseModel, constr


class UserBase(BaseModel):
    reddit: Optional[constr(min_length=2)] = None
    instagram: Optional[constr(min_length=2)] = None
    twitter: Optional[constr(min_length=2)] = None


class UserCreate(UserBase):
    name: constr(min_length=3)


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    name: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

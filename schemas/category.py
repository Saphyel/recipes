from pydantic import BaseModel


class CategoryBase(BaseModel):
    pass


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    name: str

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass

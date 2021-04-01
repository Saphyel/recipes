from pydantic import BaseModel, constr


class CategoryBase(BaseModel):
    pass


class CategoryCreate(CategoryBase):
    name: constr(min_length=3)


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    name: str

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass

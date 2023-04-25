from app.schemas.base import CustomBaseModel
from pydantic import validator
import re


class Category(CustomBaseModel):
    name: str
    slug: str

    @validator('slug')
    def valited_slug(cls, value):
        if not re.match('^([a-z]|[0-9]|-|_)+$', value):
            raise ValueError('Invalid slug')
        return value
    

class CategoryOutput(Category):
    id: int

    class Config:
        orm_mode=True
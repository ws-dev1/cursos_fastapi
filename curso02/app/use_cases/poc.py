from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.category import CategoryOutput
from app.db.models import Category as CategoryModel
from fastapi_pagination import add_pagination, paginate, Page, LimitOffsetPage, Params, LimitOffsetParams
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

def list_category_uc(page: int= 1, size: int = 50):
    categories = [
        CategoryOutput(name=f'category {n}', slug=f'category-{n}', id=n)
        for n in range(100)
    ]

    params = Params(page=page, size=size)
    return paginate(categories, params=params)
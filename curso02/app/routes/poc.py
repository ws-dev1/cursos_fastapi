from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.category import CategoryOutput
from app.db.models import Category as CategoryModel
from fastapi_pagination import add_pagination, paginate, Page, LimitOffsetPage, Params, LimitOffsetParams
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from app.use_cases.poc import list_category_uc
from app.routes.custom_paginate import CustomPage, custom_sqlalchemy_paginate

router = APIRouter(prefix='/poc', tags=['POC'])

@router.get('/list', response_model=Page[CategoryOutput])
@router.get('/list/limit-offset', response_model=LimitOffsetPage[CategoryOutput])
def list_category(page: int= 1, size: int = 50):
    return list_category_uc(page=page, size=size)

@router.get('/list/sqlalchemy', response_model=CustomPage[CategoryOutput])
#@router.get('/list/limit-offset/sqlalchemy', response_model=LimitOffsetPage[CategoryOutput])
def list_category_sqlalchemy(db_session: Session = Depends(get_db_session)):
    categories = db_session.query(CategoryModel)

    return custom_sqlalchemy_paginate(categories)


add_pagination(router)
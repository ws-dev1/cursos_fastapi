from fastapi import APIRouter, Depends, Response, status, Query
from app.schemas.category import Category
from app.schemas.category import CategoryOutput
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, auth
from app.use_cases.category import CategoryUseCases
from typing import List
from fastapi_pagination import Page, add_pagination, Params



router = APIRouter(prefix='/category', tags=['Category'], dependencies=[Depends(auth)])

@router.post('/add', status_code=status.HTTP_201_CREATED, description="Add new category")
def add_category(category: Category, db_session: Session = Depends(get_db_session)):
    
    uc = CategoryUseCases(db_session=db_session)
    uc.add_category(category=category)
    return  Response(status_code=status.HTTP_201_CREATED)

@router.get('/list', response_model=Page[CategoryOutput], description="List categories")
def list(
    size: int = Query(50, ge=1, le=100, description="Size number"),
    page: int = Query(1, ge=1,  description="Size number"), 
    db_session: Session = Depends(get_db_session)
    ):
    uc = CategoryUseCases(db_session=db_session)
    response  = uc.list_categories(page=page, size=size)

    return response


@router.delete('/delete/{id}', description="Delete category")
def delete_category(id: int, db_session: Session = Depends(get_db_session)):
    uc = CategoryUseCases(db_session=db_session)
    uc.delete_category(id=id)

    return Response(status_code=status.HTTP_200_OK)



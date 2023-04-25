from fastapi import APIRouter, Depends, Response, status, Query
from app.schemas.category import Category
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, auth
from app.use_cases.product import ProductUseCases
from app.schemas.product import Product, ProductInput, ProductOutput
from fastapi_pagination import Page
from typing import List 


router = APIRouter(prefix='/product', tags=['Product'], dependencies=[Depends(auth)])

@router.post('/add', status_code=status.HTTP_201_CREATED, description="Add new product")
def add_product(produc_input: ProductInput, db_session: Session = Depends(get_db_session)):
    uc = ProductUseCases(db_session=db_session)
    uc.add_product(product=produc_input.product, category_slug=produc_input.category_slug)

    return Response(status_code=status.HTTP_201_CREATED)

@router.put('/update/{id}', description="Update product")
def update_product(id:int, product: Product, db_session: Session = Depends(get_db_session)):
    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=id, product=product)

    return Response(status_code=status.HTTP_200_OK)

@router.delete('/delete/{id}', description="Delete product")
def delete_product(id:int,db_session: Session = Depends(get_db_session)):
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/list', response_model=Page[ProductOutput], description="List products")
def list_product( page:int = Query(1, ge=1, description='page Number'), size:int= Query(50,ge=1, le=100, description='Size of page' ), search: str ='', db_session: Session = Depends(get_db_session)):
    uc = ProductUseCases(db_session=db_session)
    products = uc.list_product(page=page, size=size, search=search)

    return products



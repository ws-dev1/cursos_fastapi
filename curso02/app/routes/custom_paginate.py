from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from typing import TypeVar, Generic, Sequence, Any, Optional
from fastapi_pagination import Params
from fastapi import Query
from pydantic import BaseModel
from fastapi_pagination.utils import verify_params
from sqlalchemy.orm import Query as QueryOrm

T = TypeVar("T")

class CustomParams(BaseModel, AbstractParams):
    current_page: int = Query(1, ge=1, description="Page number")
    items_per_page: int = Query(50, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.items_per_page,
            offset=self.items_per_page * (self.current_page - 1),
        )


class CustomPage(AbstractPage[T], Generic[T]):
    current_page: int
    items_per_page: int
    item: Sequence
    __params_type__ = CustomParams

    @classmethod
    def created(cls, items: Sequence[T], params: AbstractParams, **kwargs: Any):
        return cls(
            items=items,
            current_page=params.current_page,
            item_per_page=params.items_per_page,
            **kwargs
        )

def paginate_query(query: T, params: AbstractParams) -> T:
    raw_params= params.to_raw_params().as_limit_offset()
    return query.limit(raw_params.limit).offset(raw_params.offset)

def custom_sqlalchemy_paginate(
    query: QueryOrm[Any],
    params: Optional[AbstractParams] = None,
) -> Any:
    params, _ = verify_params(params, "limit-offset")

    items = paginate_query(query, params).all()
    return CustomPage.create(items=items, params=params)
    

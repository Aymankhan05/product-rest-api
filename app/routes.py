from fastapi import APIRouter, status

from .schemas import ProductCreate, ProductResponse, ProductUpdate
from .services import (
    create_product,
    get_all_products,
    get_product,
    update_product,
    patch_product,
    delete_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(product: ProductCreate):
    return create_product(product)


@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_all():
    return get_all_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_one(product_id: int):
    return get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update(product_id: int, product: ProductCreate):
    return update_product(product_id, product)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def patch(product_id: int, product: ProductUpdate):
    return patch_product(product_id, product)


@router.delete(
    "/{product_id}",
)
def delete(product_id: int):
    return delete_product(product_id)
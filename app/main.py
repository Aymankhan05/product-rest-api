"""
Professional Product REST API.

Features:
- CRUD operations
- Pagination
- Keyword search
- Category filtering
- Price filtering
- Sorting
- Configurable result limits
- Pagination metadata
- SQLite database
- Automatic API documentation
"""

import math
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Product
from .schemas import (
    PaginatedProductResponse,
    PaginationMetadata,
    ProductCreate,
    ProductResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Product REST API",
    description=(
        "Production-style Product REST API with CRUD operations, "
        "pagination, searching, filtering and sorting."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


@app.get(
    "/",
    tags=["Health"],
)
def root():
    """
    API health check.
    """

    return {
        "message": "Product REST API is running",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new product.
    """

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/products",
    response_model=PaginatedProductResponse,
    tags=["Products"],
)
def get_products(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number starting from 1",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Number of products per page. Maximum is 50.",
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Search products by name or description",
    ),
    category: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Filter products by category",
    ),
    min_price: float | None = Query(
        default=None,
        ge=0,
        description="Minimum product price",
    ),
    max_price: float | None = Query(
        default=None,
        ge=0,
        description="Maximum product price",
    ),
    sort_by: Literal["id", "name", "price", "category"] = Query(
        default="id",
        description="Field used for sorting",
    ),
    sort_order: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sorting direction",
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve products using pagination, search, filtering and sorting.
    """

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price.",
        )

    query = db.query(Product)

    # -------------------------
    # Keyword Search
    # -------------------------
    if search:
        search_pattern = f"%{search.strip()}%"

        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
            )
        )

    # -------------------------
    # Category Filtering
    # -------------------------
    if category:
        query = query.filter(
            func.lower(Product.category)
            == category.strip().lower()
        )

    # -------------------------
    # Price Filtering
    # -------------------------
    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    # -------------------------
    # Sorting
    # -------------------------
    sort_column = getattr(Product, sort_by)

    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # -------------------------
    # Total Count
    # -------------------------
    total_items = query.count()

    total_pages = (
        math.ceil(total_items / page_size)
        if total_items
        else 0
    )

    # -------------------------
    # Pagination
    # -------------------------
    offset = (page - 1) * page_size

    products = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "items": products,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1 and total_pages > 0,
        },
    }


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    tags=["Products"],
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a product by ID.
    """

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@app.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    tags=["Products"],
)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    """
    Update an existing product.
    """

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.category = product_data.category

    db.commit()
    db.refresh(product)

    return product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a product.
    """

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    db.delete(product)
    db.commit()

    return None
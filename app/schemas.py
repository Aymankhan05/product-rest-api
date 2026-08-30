"""
Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """
    Shared product fields.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Product description",
    )

    price: float = Field(
        ...,
        gt=0,
        description="Product price",
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product category",
    )


class ProductCreate(ProductBase):
    """
    Schema used when creating a product.
    """


class ProductResponse(ProductBase):
    """
    Schema returned by the API.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginationMetadata(BaseModel):
    """
    Pagination information returned with product results.
    """

    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedProductResponse(BaseModel):
    """
    Paginated product response.
    """

    items: list[ProductResponse]
    pagination: PaginationMetadata
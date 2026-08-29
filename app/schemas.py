from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Product name"
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Product description"
    )

    price: float = Field(
        ...,
        ge=0,
        description="Product price"
    )

    quantity: int = Field(
        ...,
        ge=0,
        description="Available quantity"
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=500
    )

    price: Optional[float] = Field(
        default=None,
        ge=0
    )

    quantity: Optional[int] = Field(
        default=None,
        ge=0
    )


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)
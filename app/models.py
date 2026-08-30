"""
SQLAlchemy database models.
"""

from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Product(Base):
    """
    Product database model.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        index=True,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    price = Column(
        Float,
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
        index=True,
    )
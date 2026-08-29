from typing import Optional

from fastapi import HTTPException, status

from .database import get_connection
from .schemas import ProductCreate, ProductUpdate


def row_to_dict(row):
    if row is None:
        return None

    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "price": row["price"],
        "quantity": row["quantity"],
    }


def create_product(product: ProductCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO products (name, description, price, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (
            product.name,
            product.description,
            product.price,
            product.quantity,
        ),
    )

    connection.commit()

    product_id = cursor.lastrowid

    row = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def get_all_products():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM products ORDER BY id"
    ).fetchall()

    connection.close()

    return [row_to_dict(row) for row in rows]


def get_product(product_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return row_to_dict(row)


def update_product(product_id: int, product: ProductCreate):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    connection.execute(
        """
        UPDATE products
        SET name = ?,
            description = ?,
            price = ?,
            quantity = ?
        WHERE id = ?
        """,
        (
            product.name,
            product.description,
            product.price,
            product.quantity,
            product_id,
        ),
    )

    connection.commit()

    row = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def patch_product(product_id: int, product: ProductUpdate):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = product.model_dump(exclude_unset=True)

    if not update_data:
        connection.close()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field is required for update",
        )

    allowed_fields = {
        "name",
        "description",
        "price",
        "quantity",
    }

    fields = []
    values = []

    for field, value in update_data.items():
        if field not in allowed_fields:
            continue

        fields.append(f"{field} = ?")
        values.append(value)

    values.append(product_id)

    query = f"""
        UPDATE products
        SET {", ".join(fields)}
        WHERE id = ?
    """

    connection.execute(query, values)
    connection.commit()

    row = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def delete_product(product_id: int):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }
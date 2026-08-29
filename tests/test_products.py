import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    from app.database import get_connection

    connection = get_connection()
    connection.execute("DELETE FROM products")
    connection.commit()
    connection.close()

    yield


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_product():
    product = {
        "name": "Laptop",
        "description": "High performance laptop",
        "price": 55000,
        "quantity": 10,
    }

    response = client.post("/products", json=product)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Laptop"
    assert data["price"] == 55000
    assert data["quantity"] == 10


def test_get_products():
    product = {
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "price": 2500,
        "quantity": 20,
    }

    client.post("/products", json=product)

    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_single_product():
    product = {
        "name": "Mouse",
        "description": "Wireless computer mouse",
        "price": 1200,
        "quantity": 15,
    }

    create_response = client.post("/products", json=product)

    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Mouse"


def test_update_product():
    product = {
        "name": "Old Laptop",
        "description": "Old laptop description",
        "price": 40000,
        "quantity": 5,
    }

    create_response = client.post("/products", json=product)

    product_id = create_response.json()["id"]

    updated_product = {
        "name": "New Laptop",
        "description": "Updated laptop description",
        "price": 60000,
        "quantity": 8,
    }

    response = client.put(
        f"/products/{product_id}",
        json=updated_product,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Laptop"
    assert response.json()["price"] == 60000


def test_patch_product():
    product = {
        "name": "Phone",
        "description": "Smartphone device",
        "price": 30000,
        "quantity": 10,
    }

    create_response = client.post("/products", json=product)

    product_id = create_response.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={"price": 28000},
    )

    assert response.status_code == 200
    assert response.json()["price"] == 28000


def test_delete_product():
    product = {
        "name": "Tablet",
        "description": "Android tablet device",
        "price": 20000,
        "quantity": 7,
    }

    create_response = client.post("/products", json=product)

    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200

    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404


def test_validation():
    invalid_product = {
        "name": "A",
        "description": "Bad",
        "price": -100,
        "quantity": -5,
    }

    response = client.post(
        "/products",
        json=invalid_product,
    )

    assert response.status_code == 422


def test_product_not_found():
    response = client.get("/products/999999")

    assert response.status_code == 404
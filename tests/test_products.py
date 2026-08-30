"""
Automated tests for the Product REST API.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_products():
    """
    Create sample products for testing.
    """

    products = [
        {
            "name": "Laptop",
            "description": "Professional laptop",
            "price": 75000,
            "category": "Electronics",
        },
        {
            "name": "Wireless Mouse",
            "description": "Bluetooth wireless mouse",
            "price": 1500,
            "category": "Electronics",
        },
        {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 3000,
            "category": "Electronics",
        },
        {
            "name": "Office Chair",
            "description": "Ergonomic office chair",
            "price": 12000,
            "category": "Furniture",
        },
    ]

    created = []

    for product in products:
        response = client.post(
            "/products",
            json=product,
        )

        if response.status_code == 201:
            created.append(response.json())

    return created


def test_root_endpoint():
    """
    Verify API health endpoint.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Product REST API is running"


def test_create_product():
    """
    Verify product creation.
    """

    product = {
        "name": "Test Laptop",
        "description": "Testing product creation",
        "price": 50000,
        "category": "Electronics",
    }

    response = client.post(
        "/products",
        json=product,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Laptop"
    assert data["price"] == 50000
    assert data["category"] == "Electronics"


def test_pagination():
    """
    Verify pagination functionality.
    """

    create_test_products()

    response = client.get(
        "/products?page=1&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 2


def test_search():
    """
    Verify keyword search.
    """

    create_test_products()

    response = client.get(
        "/products?search=Laptop"
    )

    assert response.status_code == 200

    data = response.json()

    assert any(
        "Laptop" in product["name"]
        for product in data["items"]
    )


def test_category_filter():
    """
    Verify category filtering.
    """

    create_test_products()

    response = client.get(
        "/products?category=Electronics"
    )

    assert response.status_code == 200

    data = response.json()

    assert all(
        product["category"].lower() == "electronics"
        for product in data["items"]
    )


def test_price_filter():
    """
    Verify minimum and maximum price filters.
    """

    create_test_products()

    response = client.get(
        "/products?min_price=1000&max_price=5000"
    )

    assert response.status_code == 200

    data = response.json()

    for product in data["items"]:
        assert 1000 <= product["price"] <= 5000


def test_sorting():
    """
    Verify price sorting.
    """

    create_test_products()

    response = client.get(
        "/products?sort_by=price&sort_order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    prices = [
        product["price"]
        for product in data["items"]
    ]

    assert prices == sorted(prices)


def test_invalid_price_range():
    """
    Verify invalid price range handling.
    """

    response = client.get(
        "/products?min_price=5000&max_price=1000"
    )

    assert response.status_code == 400


def test_page_size_limit():
    """
    Verify that page size cannot exceed 50.
    """

    response = client.get(
        "/products?page_size=100"
    )

    assert response.status_code == 422
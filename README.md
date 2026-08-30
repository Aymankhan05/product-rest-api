🚀 Product REST API — Task 7

Internship — Python Programming Track

Task: Task 7 — Level 2
Focus: Pagination, Filtering, Searching, Sorting & Configurable Result Limits
Technology: Python, FastAPI, SQLite, SQLAlchemy
Testing: Pytest
Deployment: Docker / Render

---

📌 Project Overview

This project is a production-style REST API developed using Python and FastAPI.

For Task 7, the existing Product REST API was enhanced with commonly required API features:

- Pagination
- Keyword searching
- Category filtering
- Price filtering
- Sorting
- Configurable result limits
- Pagination metadata
- Input validation
- API documentation
- Automated testing
- Docker deployment configuration
- Rollback documentation

The objective is to demonstrate how large collections of API data can be efficiently queried and returned in a controlled and user-friendly manner.

---

🎯 Task Objective

The objective of this task is to enhance an existing REST API with:

1. Pagination
2. Keyword search
3. Filtering
4. Sorting
5. Configurable result limits
6. Pagination metadata
7. API documentation

These features are commonly used in production applications to improve API performance, usability, and scalability.

---

🛠️ Technologies Used

Technology| Purpose
Python| Programming language
FastAPI| REST API framework
SQLite| Database
SQLAlchemy| Database ORM
Pydantic| Data validation
Pytest| Automated testing
Uvicorn| ASGI server
Docker| Containerization
Render| Deployment

---

📂 Project Structure

product-rest-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   └── test_products.py
│
├── data/
│   └── products.db
│
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── README.md
└── rollback.md

---

⚙️ Features

1. Pagination

The API supports pagination using query parameters.

Example:

GET /products?page=1&page_size=10

Parameters:

- "page" — Page number
- "page_size" — Number of records returned per page

The API limits the maximum page size to 50 to prevent unnecessarily large responses.

---

2. Keyword Search

Products can be searched using keywords.

Example:

GET /products?search=Laptop

The search checks:

- Product name
- Product description

---

3. Category Filtering

Products can be filtered by category.

Example:

GET /products?category=Electronics

Category matching is handled without depending on letter casing.

---

4. Price Filtering

Products can be filtered using minimum and maximum prices.

Minimum price

GET /products?min_price=1000

Maximum price

GET /products?max_price=5000

Price range

GET /products?min_price=1000&max_price=5000

The API validates that the minimum price is not greater than the maximum price.

---

5. Sorting

Products can be sorted by supported fields.

Supported fields:

id
name
price
category

Ascending order

GET /products?sort_by=price&sort_order=asc

Descending order

GET /products?sort_by=price&sort_order=desc

---

6. Combining API Features

Multiple query parameters can be used together.

Example:

GET /products?page=1&page_size=5&search=wireless&category=Electronics&min_price=500&max_price=5000&sort_by=price&sort_order=asc

This request combines:

Pagination
+
Search
+
Category filtering
+
Price filtering
+
Sorting

---

📊 Pagination Response

The API returns pagination metadata along with the product results.

Example:

{
  "items": [
    {
      "id": 1,
      "name": "Laptop",
      "description": "Professional laptop",
      "price": 75000,
      "category": "Electronics"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_items": 25,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  }
}

Pagination metadata includes:

- Current page
- Page size
- Total number of items
- Total number of pages
- Whether a next page exists
- Whether a previous page exists

---

🔗 API Endpoints

Method| Endpoint| Description
GET| "/"| API health check
POST| "/products"| Create product
GET| "/products"| List products with pagination/search/filter/sort
GET| "/products/{product_id}"| Get product by ID
PUT| "/products/{product_id}"| Update product
DELETE| "/products/{product_id}"| Delete product

---

📖 API Documentation

FastAPI automatically generates interactive API documentation.

After starting the server, open:

http://127.0.0.1:8000/docs

The Swagger interface can be used to:

- View endpoints
- Send API requests
- Test query parameters
- View request schemas
- View response schemas
- Test validation and error handling

---

💻 Installation

1. Clone the repository

git clone <YOUR-GITHUB-REPOSITORY-URL>

Move into the project:

cd product-rest-api

---

2. Install dependencies

python -m pip install -r requirements.txt

---

3. Start the API

python -m uvicorn app.main:app --reload

The API will run at:

http://127.0.0.1:8000

---

🧪 Testing

The project includes automated tests using Pytest.

Run:

python -m pytest -v

Test Result

9 passed

The tests verify:

- API health endpoint
- Product creation
- Pagination
- Searching
- Category filtering
- Price filtering
- Sorting
- Invalid price ranges
- Maximum page-size validation

---

🐳 Docker

The project includes a Dockerfile for containerized execution.

Build the image:

docker build -t product-rest-api .

Run the container:

docker run -p 8000:8000 product-rest-api

The API will then be available at:

http://localhost:8000

---

🐳 Docker Compose

The project also includes Docker Compose.

Run:

docker compose up --build

Stop:

docker compose down

---

☁️ Deployment

The project includes a "render.yaml" deployment configuration.

The application uses:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

for production deployment.

---

🔄 Rollback

A dedicated "rollback.md" file is included in the repository.

The documented rollback process uses Git to revert a problematic deployment.

Basic rollback command:

git revert <commit-hash>

Then push the rollback:

git push origin master

After rollback, the API should be tested again using:

- "/"
- "/docs"
- "/products"
- Pagination
- Search
- Filtering
- Sorting

---

🔐 Validation & Error Handling

The API includes request validation using Pydantic and FastAPI.

Examples of validation include:

- Product name cannot be empty
- Product price must be greater than zero
- Page number must be at least 1
- Page size must be between 1 and 50
- Search input has a reasonable length limit
- Invalid price ranges are rejected
- Unsupported sorting fields are rejected

Example:

min_price=5000
max_price=1000

returns:

HTTP 400 Bad Request

with:

{
  "detail": "min_price cannot be greater than max_price."
}

---

⚡ Performance Considerations

Pagination helps prevent the API from returning unnecessarily large datasets.

Instead of requesting thousands of products at once, clients can request smaller pages:

?page=1&page_size=10

This can reduce:

- Network bandwidth
- Response size
- Client processing
- Memory usage
- Server workload

Search and filtering also allow clients to retrieve only relevant records.

---

🧠 Key Concepts Learned

Through this task, the following API concepts were implemented:

- REST API query parameters
- Pagination
- Offset and limit
- Keyword searching
- Filtering
- Sorting
- Input validation
- Database queries
- API response metadata
- Automated API testing
- API documentation
- Docker deployment
- Git-based rollback

---

🎤 Interview Questions

1. Why is pagination important?

Pagination divides a large dataset into smaller pages, reducing response size, network traffic, memory usage, and processing time.

---

2. What is the difference between filtering and searching?

Filtering restricts results using specific conditions such as category or price.

Searching looks for a keyword across searchable fields such as product name or description.

---

3. How can large API responses affect performance?

Large API responses can increase network usage, server memory consumption, database workload, and response time.

---

4. What is a query parameter?

A query parameter is additional information passed in the URL after "?".

Example:

/products?page=2&page_size=10

Here "page" and "page_size" are query parameters.

---

5. What is pagination?

Pagination is the process of dividing a large collection of records into smaller pages.

---

6. Why limit the maximum page size?

A maximum page size prevents clients from requesting extremely large datasets that could negatively affect API performance.

---

7. What is sorting?

Sorting arranges API results according to a selected field and direction.

Example:

sort_by=price&sort_order=asc

---

8. Why return pagination metadata?

Pagination metadata tells the client about the current page, total records, total pages, and whether additional pages are available.

---

🚀 Future Improvements

Possible future improvements include:

- Authentication and authorization
- JWT-based security
- Database migrations
- PostgreSQL support
- Advanced filtering
- Full-text search
- Rate limiting
- Caching
- Logging and monitoring
- CI/CD automation
- API versioning

---

✅ Task 7 Completion

[✓] REST API
[✓] Pagination
[✓] Keyword search
[✓] Category filtering
[✓] Price filtering
[✓] Sorting
[✓] Configurable result limits
[✓] Pagination metadata
[✓] Input validation
[✓] API documentation
[✓] Automated tests
[✓] 9 tests passed
[✓] Docker configuration
[✓] Render configuration
[✓] Rollback documentation
[✓] GitHub-ready project

---

👨‍💻 Author

Ayman Khan

Python Programming Internship
Task 7 — Level 2

---

📌 Internship Deliverable

This repository demonstrates the implementation of production-oriented API features including pagination, searching, filtering, sorting, validation, testing, documentation, deployment configuration, and rollback procedures.
# Product REST API

A professional REST API for managing products using **FastAPI** and **SQLite**.

## 🚀 Features

- Create products
- Get all products
- Get a single product
- Update a complete product
- Partially update a product
- Delete products
- SQLite database
- Pydantic validation
- Automatic API documentation with Swagger UI
- ReDoc documentation
- Health check endpoint
- Docker support
- Pytest testing support

## 🛠️ Technologies Used

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Pytest
- Docker
- Git & GitHub

## 📁 Project Structure

```text
product-rest--api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── services.py
│
├── data/
│   └── products.db
│
├── tests/
│
├── .venv/
│
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.mdYes 👍 README.md being empty is the one we should fill now.
Open README.md, delete anything inside it if there is anything, and copy-paste this complete README:
# Product REST API

A professional REST API for managing products using **FastAPI** and **SQLite**.

## 🚀 Features

- Create products
- Get all products
- Get a single product
- Update a complete product
- Partially update a product
- Delete products
- SQLite database
- Pydantic validation
- Automatic API documentation with Swagger UI
- ReDoc documentation
- Health check endpoint
- Docker support
- Pytest testing support

## 🛠️ Technologies Used

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Pytest
- Docker
- Git & GitHub

## 📁 Project Structure

```text
product-rest--api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── services.py
│
├── data/
│   └── products.db
│
├── tests/
│
├── .venv/
│
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
⚙️ Installation
Clone the repository:
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd product-rest--api
Create a virtual environment:
python -m venv .venv
Windows PowerShell
Activate the virtual environment:
.venv\Scripts\Activate.ps1
If PowerShell blocks activation, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Then:
.venv\Scripts\Activate.ps1
Install dependencies:
python -m pip install -r requirements.txt
▶️ Run the Application
Start the FastAPI server:
python -m uvicorn app.main:app --reload
The API will run at:
http://127.0.0.1:8000
📚 API Documentation
Swagger UI
Open:
http://127.0.0.1:8000/docs
ReDoc
Open:
http://127.0.0.1:8000/redoc
🔗 API Endpoints
Method
Endpoint
Description
GET
/
API information
GET
/health
Health check
POST
/products
Create a product
GET
/products
Get all products
GET
/products/{product_id}
Get one product
PUT
/products/{product_id}
Update a product
PATCH
/products/{product_id}
Partially update a product
DELETE
/products/{product_id}
Delete a product
📦 Create Product
Request
POST /products
Example Body
{
  "name": "Laptop",
  "description": "High performance laptop",
  "price": 55000,
  "quantity": 10
}
Example Response
{
  "id": 1,
  "name": "Laptop",
  "description": "High performance laptop",
  "price": 55000,
  "quantity": 10
}
🔍 Get All Products
GET /products
Example response:
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High performance laptop",
    "price": 55000,
    "quantity": 10
  }
]
✏️ Update Product
PUT /products/1
Example:
{
  "name": "Gaming Laptop",
  "description": "High performance gaming laptop",
  "price": 65000,
  "quantity": 8
}
🔧 Partial Update
PATCH /products/1
Example:
{
  "name": "Gaming Laptop",
  "description": "High performance gaming laptop",
  "price": 60000,
  "quantity": 8
}
🗑️ Delete Product
DELETE /products/1
A successful deletion returns:
204 No Content
❤️ Health Check
GET /health
Example response:
{
  "status": "healthy",
  "service": "Product REST API"
}
🗄️ Database
The application uses SQLite for persistent product storage.
Database location:
data/products.db
The database and products table are automatically initialized when the application starts.
🧪 Testing
Run the test suite using:
pytest
The tests verify the API's main CRUD functionality and validation behavior.
🐳 Docker
Build the Docker image:
docker build -t product-rest-api .
Run the container:
docker run -p 8000:8000 product-rest-api
Then open:
http://localhost:8000/docs
📋 HTTP Status Codes
Status Code
Meaning
200
Successful request
201
Product created
204
Product deleted
404
Product not found
422
Validation error
500
Internal server error
🎯 Project Objective
The objective of this project is to demonstrate how to build a structured REST API using FastAPI with SQLite database integration, validation, CRUD operations, automated documentation, testing, and Docker support.
👨‍💻 Author
Ayman Khan
📄 License
This project is created for educational and portfolio purposes.

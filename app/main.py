from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import initialize_database
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    print("Database initialized successfully.")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Product REST API",
    description=(
        "A professional REST API providing CRUD operations "
        "for products using FastAPI and SQLite."
    ),
    version="1.0.0",
)


app.include_router(router)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "Product REST API is running",
        "documentation": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "service": "Product REST API",
    }
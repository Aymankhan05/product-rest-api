# ============================================================
# PRODUCT REST API - DOCKERFILE
# ============================================================

FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Send Python output directly to the terminal
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Copy dependency file first for better Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

# Create database directory
RUN mkdir -p /app/data

# Expose FastAPI port
EXPOSE 8000

# Start production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
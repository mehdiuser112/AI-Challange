# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# Install system dependencies first
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install requirements with detailed logging
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 2>&1 | tee pip_install.log

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "model.py"]



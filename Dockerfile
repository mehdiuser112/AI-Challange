# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip with verbose output
RUN python -m pip install --upgrade pip --verbose

# Install Python dependencies with verbose output
RUN python -m pip install --no-cache-dir -r requirements.txt --verbose

# Run the application
CMD ["python", "model.py"]


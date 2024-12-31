# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install each requirement separately with verbose output
RUN pip install --upgrade pip && \
    pip install pyTelegramBotAPI==4.12.0 --verbose && \
    pip install huggingface_hub==0.27.0 --verbose && \
    pip install Pillow==9.5.0 --verbose && \
    pip install python-dotenv==1.0.0 --verbose

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "model.py"]


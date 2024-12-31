# Use an official Python runtime as a parent image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Make sure the virtual environment is the default Python
ENV PATH="/opt/venv/bin:$PATH"

# Expose port (if your bot needs it, otherwise remove this line)
EXPOSE 5000

# Define the command to run the bot
CMD ["python", "model.py"]

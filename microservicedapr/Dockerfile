# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install curl for health checks and Dapr CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Install Dapr CLI
#RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Expose the port for the application
EXPOSE 5000

# Command to run the application with Dapr
# Note: Actual Dapr sidecar will be injected by Dapr runtime in deployment
CMD ["python", "app.py"]

# To run with Dapr locally:
# dapr run --app-id myapp --app-port 5000 --dapr-http-port 3500 python app.py

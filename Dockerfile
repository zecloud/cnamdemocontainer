# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . /app

# Expose the port Chainlit runs on
EXPOSE 8000

# Command to run on container start
CMD ["chainlit", "run", "app.py", "--port=8000", "--host=0.0.0.0"]

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root directory
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the inference service
COPY inference/ ./inference/

# Copy models directory
COPY models/ ./models/

# Expose the API port
EXPOSE 8000

# Run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "inference.app:app"]
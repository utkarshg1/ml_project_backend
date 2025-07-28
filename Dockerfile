# Use slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv using pip (Python-based version)
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for Docker cache)
COPY pyproject.toml uv.lock* ./

# Install Python dependencies using uv
RUN uv sync

# Copy the rest of your code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]

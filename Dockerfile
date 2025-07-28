FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl and uv
RUN apt-get update && \
    apt-get install -y curl && \
    curl -Ls https://astral.sh/uv/install.sh | bash && \
    apt-get purge -y curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock* ./

# Sync dependencies
RUN /root/.cargo/bin/uv sync

# Copy rest of the app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

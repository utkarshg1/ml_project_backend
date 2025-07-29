# Simple Dockerfile with uv - copy everything and sync
FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies with uv
RUN uv sync

# Make sure we use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
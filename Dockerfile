# 🧱 Stage 1: Builder using uv for dependency resolution
FROM python:3.12-slim-bookworm AS builder

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy lockfile and dependencies manifest
COPY pyproject.toml uv.lock* /app/

# Install dependencies (without project code) for cache efficiency
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy code and sync project (non-editable)
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# 🧱 Stage 2: Final slimmer runtime image
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app
COPY --from=builder /app /app

# Make sure project's virtualenv is in PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl and uv
RUN apt-get update && \
    apt-get install -y curl && \
    curl -Ls https://astral.sh/uv/install.sh | bash && \
    mv ~/.cargo/bin/uv /usr/local/bin/uv && \
    apt-get purge -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Multi-stage Dockerfile for Enterprise Pharmaceutical Ecosystem
# Builds both Vite React Frontend and FastAPI Backend into a single production container

# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /web
COPY apps/web/package*.json ./
RUN npm ci
COPY apps/web/ ./
RUN npm run build

# Stage 2: Backend & Unified Application Runtime
FROM python:3.12-slim AS backend

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app:/app/src"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY apps/ ./apps/
COPY tests/ ./tests/
RUN mkdir -p /app/data

# Copy compiled React frontend assets from Stage 1
COPY --from=frontend-builder /web/dist /app/apps/web/dist

RUN pip install --no-cache-dir -e .

EXPOSE 8000

# Runs on dynamic port (compatible with Render, Hugging Face, Railway, Fly.io, or local Docker)
CMD ["sh", "-c", "uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

# Landslide Backend

FastAPI backend for landslide risk assessment and resource allocation.

## Setup

1. Copy `.env.example` to `.env` and update values
2. Start services: `docker compose up -d`
3. Run: `uv run --package landslide-backend uvicorn landslide_backend.main:app --reload`

## API Documentation

Once running, visit http://localhost:8000/docs for Swagger UI.

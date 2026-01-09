# gq-kp-fastapi

FastAPI rewrite of the existing `gq-kp-api` (.NET) backend.

## Features
- Brands CRUD: `/api/brands`
- Products CRUD + search: `/api/products`, `/api/products/search?q=...`
- Excel import: `/api/import/products` (upload `.xlsx`)

## Configuration
Uses environment variables:
- `DATABASE_URL` (required) e.g. `postgresql+psycopg://postgres:password@localhost:5432/gqkp`
- `CORS_ORIGINS` (optional) comma-separated, default: `http://localhost:5059`

## Run (development)
Create a virtualenv, install deps, run migrations, start the server.

### Start Postgres (recommended: Docker)
This repo includes a `docker-compose.yml` that starts Postgres with a pre-created database `gqkp`.

```bash
cd py-backend
docker compose up -d
```

Then copy env file:

```bash
cp .env.example .env
```

Example commands (optional):

```bash
cd py-backend
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"

# Optional: migrations (tables are also auto-created on startup)
# alembic upgrade head

# Start API
uvicorn app.main:app --reload --port 8000
```

Swagger UI:
- http://localhost:8000/docs

## Excel import
POST an Excel file. The importer reads the first sheet and maps columns by headers, with fallbacks.

```bash
curl -F "file=@/path/to/products.xlsx" http://localhost:8000/api/import/products
```
# openbook_backend

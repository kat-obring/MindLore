# MindLore

AI assistant for social content ideation and polishing. Tech stack: FastAPI (backend), React + Vite + TypeScript + Tailwind (frontend), Claude for generation.

## Prerequisites

- Python 3.12+
- Node.js 20+ and npm
- Docker (optional, for containerized development)

## Setup

1) Copy `env.example` to `.env` and fill in secrets (e.g., `CLAUDE_API_KEY`).

2) Install dependencies:

```bash
make install          # backend (pip editable dev) + frontend (npm install)
```

Backend-only or frontend-only installs:

```bash
make backend-install
make frontend-install
```

## Lint and Test

```bash
make lint   # backend: ruff check + ruff format --check; frontend: eslint
make test   # backend: pytest; frontend: vitest
```

Run tests separately:

- Backend: `make backend-test` (or `cd backend && pytest`)
- Frontend: `make frontend-test` (or `cd frontend && npm test -- --run`)
- All tests: `make test`

Lint/check locally with the same commands CI uses:

```bash
# backend
cd backend
.venv/bin/ruff check .
.venv/bin/ruff format --check .

# frontend
cd frontend
npm run lint
```

## Run Locally

- Frontend dev server:

```bash
cd frontend
npm run dev
```

- Backend app (requires `CLAUDE_API_KEY` set):
  - From `backend/`: `uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000`
  - Or use Make target: `make backend-serve` (respects `PORT` env/var)

## Run with Docker

Start both frontend and backend with a single command:

```bash
docker compose up
```

This starts:
- Frontend at http://localhost:5173 (with hot reload)
- Backend at http://localhost:8000 (with hot reload)

Other useful commands:

```bash
docker compose up -d        # Run in background
docker compose down         # Stop all containers
docker compose logs -f      # Follow logs
docker compose up --build   # Rebuild after Dockerfile changes
```

## API Docs (Swagger)

When the backend is running, Swagger UI is available at:

- `http://localhost:8000/docs`

The OpenAPI schema is available at:

- `http://localhost:8000/openapi.json`

## CI

GitHub Actions workflow runs lint and tests for backend and frontend on pushes/PRs to main/master.

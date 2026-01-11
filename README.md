# MindLore

AI assistant for social content ideation and polishing. Tech stack: FastAPI (backend), React + Vite + TypeScript + Tailwind (frontend), OpenAI ChatGPT 5.2 for generation.

## Prerequisites

- Python 3.11+
- Node.js 20+ and npm

## Setup

1) Copy `env.example` to `.env` and fill in secrets (e.g., `OPENAI_API_KEY`).

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
make lint   # ruff + black --check (backend), eslint (frontend)
make test   # pytest (backend), vitest (frontend)
```

## Run Locally

- Frontend dev server:

```bash
cd frontend
npm run dev
```

- Backend app (requires `OPENAI_API_KEY` set):
  - From `backend/`: `uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000`
  - Or use Make target: `make backend-serve` (respects `PORT` env/var)

## CI

GitHub Actions workflow runs lint and tests for backend and frontend on pushes/PRs to main/master.

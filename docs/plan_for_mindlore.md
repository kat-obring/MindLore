---
name: Plan for AI content assistant (Python/SQLite, no auth)
overview: Design and build the content creation assistant using Python backend (FastAPI), SQLite for now, no auth. Frontend likely React/Next for UI, with upgrade path to Postgres later.
todos:
  - id: scaffold-backend
    content: Scaffold FastAPI app + models + migrations
    status: pending
  - id: scaffold-frontend
    content: Set up Next.js UI shell
    status: pending
  - id: idea-crud
    content: Implement idea CRUD API + UI
    status: pending
    dependencies:
      - scaffold-backend
      - scaffold-frontend
  - id: style-guides
    content: Load/style guide listing endpoint
    status: pending
    dependencies:
      - scaffold-backend
  - id: angle-gen
    content: Angles generation API + UI display
    status: pending
    dependencies:
      - idea-crud
      - style-guides
  - id: draft-gen
    content: Draft generation API + channel selection
    status: pending
    dependencies:
      - angle-gen
  - id: editor-save
    content: Draft editing UI + save
    status: pending
    dependencies:
      - draft-gen
  - id: ci-docker
    content: CI pipeline + Docker packaging
    status: pending
    dependencies:
      - scaffold-backend
      - scaffold-frontend
---

# Plan: AI Content Assistant (FastAPI + SQLite, no auth)

## Stack decisions

- Backend: FastAPI + SQLModel/SQLAlchemy; SQLite dev default; design for easy Postgres swap later (env-driven URL, Alembic migrations).
- Frontend: React/Next.js SPA consuming REST API (or HTMX-lite if we stay server-rendered; default to React/Next for UI richness).
- Infra: Docker for app + db; CI to run tests/lint.

## Architecture (high level)

```mermaid
flowchart TD
  user[User] --> ui[Next.js UI]
  ui --> api[FastAPI]
  api --> db[SQLite (dev) / Postgres (prod ready)]
  api --> openai[OpenAI API]
  styleGuides[Markdown style guides] --> api
```

## Deliverables by stage

1) **Project scaffolding**: FastAPI app with SQLModel models, migrations via Alembic, health check, Dockerfile + docker-compose (app + SQLite volume). Next app with basic layout.

2) **Content idea CRUD**: API + UI to create/list/select ideas; status fields; tests.

3) **Style guide ingestion**: Read .md files from repo/storage; API endpoint to list/apply guides.

4) **Angle generation**: Endpoint to send idea + style guide to OpenAI; return 3 options; display in UI; store responses.

5) **Selection & draft generation**: Choose an option; generate full draft for target channel (blog/LinkedIn/Bluesky/email); persist draft version.

6) **Editing & saving**: UI text editor; save edits back to DB; history/versioning minimal (last_saved_at + content field, optional revisions table).

7) **Testing & CI**: Unit tests (backend + frontend); e2e smoke; GitHub Actions/CI to run tests/lint; pre-commit hooks optional.

8) **Packaging**: Docker images for backend/front; env-based config; optional prod profile to swap SQLite → Postgres.

## Data model (initial)

- `Idea`: id, title, description, status (new, angles_generated, draft_ready, published), created_at.
- `StyleGuide`: id, name, path/origin, content (cached), created_at.
- `AngleOption`: id, idea_id FK, guide_id FK, text, rank/order, created_at.
- `Draft`: id, idea_id FK, guide_id FK, chosen_angle_id FK nullable, channel (blog/linkedin/bluesky/email), content, created_at, updated_at.

## API surface (v1)

- `GET /health`
- `POST /ideas` / `GET /ideas`
- `POST /ideas/{id}/angles` (inputs: styleGuideId, maybe temperature); returns 3 options
- `POST /ideas/{id}/draft` (inputs: chosenAngleId, channel)
- `PATCH /drafts/{id}` (save edits)
- `GET /style-guides` (list names/ids)

## Frontend slices

- Ideas list + create form
- Idea detail: generate angles, show options, select one
- Draft view/editor: show generated draft, channel selector, save button

## Testing strategy

- Backend: pytest for models/services; test OpenAI client via stub
- Frontend: component tests (Vitest/RTL), light e2e (Playwright) for core flow
- CI: run lint + tests for both apps; optional type checks (mypy/pyright, ts types)

## Notes on DB choice

- SQLite keeps dev simple; concurrency is limited but fine for single-user dev. Schema is portable; use env `DATABASE_URL` so swapping to Postgres later is one variable + migration run.

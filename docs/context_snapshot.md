# Context Snapshot (dev progress)

- **Backend**: FastAPI + SQLModel. `create_app()` loads `.env`, uses `DATABASE_URL` (default `sqlite:///./app.db`), `OPENAI_API_KEY` / `OPENAI_MODEL` (default `gpt-4o-mini`, stubbed client if no key), `STYLE_GUIDES_PATH` (default `docs/styleguides`), `CORS_ORIGINS` (default `http://localhost:3000`, `http://127.0.0.1:3000`). Endpoints: `/health`, `/ideas` POST/GET, `/style-guides`, `/ideas/{id}/angles` (OpenAI-backed).
- **DB**: `Idea` allows nullable description; dropping `app.db` recreates schema. No migrations yet.
- **Frontend**: Next.js app in `web/` with `TopicApp` for adding/listing ideas (title only). Uses `NEXT_PUBLIC_API_BASE` (default `http://localhost:8000`). Vitest test `tests/topic-app.test.tsx` passes.
- **Plan**: `docs/plan.md` — Tests 1-7 done; next: Test 8 (draft generation via OpenAI + persistence), Test 9 (draft edit), Test 10 (CI runs frontend tests).
- **CI**: currently only backend (ruff + pytest). Needs frontend job to run Vitest in `web/`.
- **Env**: Keep `.env` in repo root (git-ignored) per `docs/env.example`. OpenAI key now loads correctly.
- **Style guides**: place `.md` files in `docs/styleguides/`; exposed via `/style-guides`.
- **Note**: Next 14.2.15 has a security advisory; consider bumping to patched release later.

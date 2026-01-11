# Style Guides

Place markdown style guides in this folder. Each `.md` file is exposed by `GET /style-guides` using its stem as the `name`.

Example files you can add:
- `friendly.md`
- `concise.md`
- `technical.md`

## Run the app locally

Backend (FastAPI):
- `cd /Users/katobring/Documents/code/MindLore`
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- copy `docs/env.example` to `.env` (set `OPENAI_API_KEY` if you want real calls)
- `uvicorn app.main:app --reload --port 8000`

Frontend (Next.js):
- `cd /Users/katobring/Documents/code/MindLore/web`
- `npm install`
- `npm run dev` (uses `NEXT_PUBLIC_API_BASE` default `http://localhost:8000`)

Check style guides endpoint:
- `curl http://localhost:8000/style-guides`

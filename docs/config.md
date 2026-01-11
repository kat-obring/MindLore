# Configuration

Set environment variables (e.g., in a local `.env` not committed):

- `OPENAI_API_KEY`: your OpenAI API key.
- `OPENAI_MODEL`: model name (default `gpt-4o-mini`).
- `DATABASE_URL`: database URL (default `sqlite:///./app.db`).
- `STYLE_GUIDES_PATH`: path to folder of `.md` style guides (default `docs/styleguides`).

Example `.env` (do not commit):
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
DATABASE_URL=sqlite:///./app.db
STYLE_GUIDES_PATH=docs/styleguides
```

from pathlib import Path

from fastapi import Depends
from sqlalchemy.engine.url import make_url
from sqlmodel import SQLModel

from ..core.config import Settings, get_settings
from ..core.db import get_engine, get_session
from ..prompts.repository import FilePromptRepository
from ..suggestions.service import ClaudeClient, LLMClient, SuggestionService


def get_prompt_repository() -> FilePromptRepository:
    settings = get_settings()
    return FilePromptRepository(prompts_dir=settings.prompts_dir)


def get_llm_client() -> LLMClient:
    settings = get_settings()
    # In a real app, we might check APP_ENV or similar
    # For now, if we have a real key, we can use the real client
    # but for tests, we will use dependency_overrides.
    return ClaudeClient(api_key=settings.claude_api_key, model=settings.claude_model)


def get_suggestion_service() -> SuggestionService:
    return SuggestionService(get_prompt_repository(), get_llm_client())


async def get_session_dep(settings: Settings = Depends(get_settings)):  # noqa: B008
    _ensure_sqlite_dir(settings.database_url)
    engine = get_engine(settings)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with get_session(engine) as session:
        yield session


def _ensure_sqlite_dir(database_url: str) -> None:
    url = make_url(database_url)
    if url.drivername.startswith("sqlite") and url.database:
        path = Path(url.database)
        if not path.is_absolute():
            path = Path.cwd() / path
        path.parent.mkdir(parents=True, exist_ok=True)

import pytest
from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from sqlmodel import text


@pytest.mark.asyncio
async def test_get_session_runs_simple_query(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    settings = Settings(
        _env_file=None,
        claude_api_key="sk-test",
        database_url=f"sqlite+aiosqlite:///{db_path}",
    )

    engine = get_engine(settings)

    async with get_session(engine) as session:
        result = await session.exec(text("SELECT 1"))
        assert result.one()[0] == 1

import pytest
from backend.app.core.config import get_settings
from backend.app.core.db import get_engine
from backend.app.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlmodel import SQLModel


@pytest.mark.asyncio
async def test_startup_creates_tables(tmp_path, monkeypatch):
    db_path = tmp_path / "startup.db"
    monkeypatch.setenv("OPENAI_API_KEY", "sk-startup")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")
    get_settings.cache_clear()

    app = create_app()
    with TestClient(app):
        pass  # entering context triggers lifespan/startup

    settings = get_settings()
    engine = get_engine(settings)

    async with engine.begin() as conn:

        def _get_tables(sync_conn):
            insp = inspect(sync_conn)
            return insp.get_table_names()

        tables = await conn.run_sync(_get_tables)

    # Ensure all SQLModel tables are created
    expected_tables = set(SQLModel.metadata.tables.keys())
    assert expected_tables.issubset(set(tables))

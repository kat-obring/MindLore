import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel, select

from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from backend.app.main import create_app
from backend.app.models import Topic
from backend.app.api.dependencies import get_session_dep, get_settings


@pytest.mark.asyncio
async def test_post_topic_persists_and_returns_topic(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    settings = Settings(
        _env_file=None,
        openai_api_key="sk-test",
        database_url=f"sqlite+aiosqlite:///{db_path}",
    )
    engine = get_engine(settings)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings

    async def override_session_dep():
        async with get_session(engine) as session:
            yield session

    app.dependency_overrides[get_session_dep] = override_session_dep

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/topics", json={"title": "My Topic", "detail": "Details"}
        )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "My Topic"
    assert body["detail"] == "Details"
    assert body["id"] is not None

    async with get_session(engine) as verify_session:
        result = await verify_session.exec(select(Topic))
        saved = result.one()
        assert saved.title == "My Topic"
        assert saved.detail == "Details"

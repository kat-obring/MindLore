import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel, select

from backend.app.api.dependencies import (
    get_session_dep,
    get_settings,
    get_suggestion_service,
)
from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from backend.app.main import create_app
from backend.app.models import Suggestion, Topic


class FakeSuggestionService:
    def get_suggestions(self, topic: str):
        return [
            "### Outline A: Angle 1",
            "### Outline B: Angle 2",
            "### Outline C: Angle 3",
        ]


@pytest.mark.asyncio
async def test_post_suggestions_persists_topic_and_suggestions(tmp_path) -> None:
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
    app.dependency_overrides[get_suggestion_service] = lambda: FakeSuggestionService()

    async def override_session_dep():
        async with get_session(engine) as session:
            yield session

    app.dependency_overrides[get_session_dep] = override_session_dep

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/suggestions", json={"topic": "Persisted Topic"}
        )

    assert response.status_code == 200
    body = response.json()
    assert body["suggestions"] == [
        "### Outline A: Angle 1",
        "### Outline B: Angle 2",
        "### Outline C: Angle 3",
    ]

    async with get_session(engine) as verify_session:
        topic_result = await verify_session.exec(select(Topic))
        saved_topic = topic_result.one()
        assert saved_topic.title == "Persisted Topic"

        suggestion_result = await verify_session.exec(
            select(Suggestion)
            .where(Suggestion.topic_id == saved_topic.id)
            .order_by(Suggestion.position)
        )
        saved_suggestions = suggestion_result.all()
        assert [s.content for s in saved_suggestions] == [
            "### Outline A: Angle 1",
            "### Outline B: Angle 2",
            "### Outline C: Angle 3",
        ]
        assert [s.position for s in saved_suggestions] == [0, 1, 2]

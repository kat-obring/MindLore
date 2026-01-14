import pytest
from sqlmodel import SQLModel, select

from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from backend.app.models.suggestion import Suggestion
from backend.app.models.topic import Topic


@pytest.mark.asyncio
async def test_suggestion_persists_with_topic_fk(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    settings = Settings(
        _env_file=None,
        openai_api_key="sk-test",
        database_url=f"sqlite+aiosqlite:///{db_path}",
    )
    engine = get_engine(settings)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with get_session(engine) as session:
        topic = Topic(title="My Topic", detail="Details")
        session.add(topic)
        await session.commit()
        await session.refresh(topic)

        s1 = Suggestion(topic_id=topic.id, content="Suggestion A", position=0)
        s2 = Suggestion(topic_id=topic.id, content="Suggestion B", position=1)
        session.add_all([s1, s2])
        await session.commit()

        result = await session.exec(
            select(Suggestion)
            .where(Suggestion.topic_id == topic.id)
            .order_by(Suggestion.position)
        )
        saved = result.all()

        assert [s.content for s in saved] == ["Suggestion A", "Suggestion B"]
        assert all(s.id is not None for s in saved)
        assert all(s.topic_id == topic.id for s in saved)

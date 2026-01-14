import pytest
from sqlmodel import SQLModel, select

from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from backend.app.models.topic import Topic


@pytest.mark.asyncio
async def test_topic_round_trip(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    settings = Settings(
        _env_file=None,
        openai_api_key="sk-test",
        database_url=f"sqlite+aiosqlite:///{db_path}",
    )
    engine = get_engine(settings)

    # Create tables for the test database
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with get_session(engine) as session:
        topic = Topic(title="My Topic", detail="Details here")
        session.add(topic)
        await session.commit()
        await session.refresh(topic)

        result = await session.exec(select(Topic))
        saved = result.one()

        assert saved.id is not None
        assert saved.title == "My Topic"
        assert saved.detail == "Details here"

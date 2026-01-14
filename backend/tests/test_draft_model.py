import pytest
from sqlmodel import SQLModel, select

from backend.app.core.config import Settings
from backend.app.core.db import get_engine, get_session
from backend.app.models.draft import Draft
from backend.app.models.topic import Topic


@pytest.mark.asyncio
async def test_draft_persists_with_topic_fk(tmp_path) -> None:
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
        topic = Topic(title="Topic", detail="Detail")
        session.add(topic)
        await session.commit()
        await session.refresh(topic)

        draft = Draft(
            topic_id=topic.id,
            content="Draft body",
            selected_suggestion_index=1,
        )
        session.add(draft)
        await session.commit()
        await session.refresh(draft)

        result = await session.exec(select(Draft).where(Draft.topic_id == topic.id))
        saved = result.one()

        assert saved.id is not None
        assert saved.content == "Draft body"
        assert saved.topic_id == topic.id
        assert saved.selected_suggestion_index == 1

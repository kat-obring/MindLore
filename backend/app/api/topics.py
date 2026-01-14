from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from sqlmodel.ext.asyncio.session import AsyncSession

from ..api.dependencies import get_session_dep
from ..models import Topic

router = APIRouter(prefix="/api")


class TopicCreate(BaseModel):
    title: str = Field(..., min_length=1)
    detail: str = ""

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip()

    @field_validator("detail")
    @classmethod
    def detail_trim(cls, v: str) -> str:
        return v.strip()


class TopicRead(BaseModel):
    id: int
    title: str
    detail: str

    model_config = {"from_attributes": True}


@router.post("/topics", response_model=TopicRead)
async def create_topic(
    payload: TopicCreate,
    session: Annotated[AsyncSession, Depends(get_session_dep)],
) -> TopicRead:
    topic = Topic(title=payload.title, detail=payload.detail)
    session.add(topic)
    await session.commit()
    await session.refresh(topic)
    return TopicRead.model_validate(topic)

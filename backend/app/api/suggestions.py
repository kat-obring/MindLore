from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlmodel.ext.asyncio.session import AsyncSession

from .dependencies import get_session_dep, get_suggestion_service
from ..models import Suggestion, Topic
from ..suggestions.service import SuggestionService

router = APIRouter(prefix="/api")


class SuggestionRequest(BaseModel):
    topic: str = Field(..., min_length=1)

    @field_validator("topic")
    @classmethod
    def topic_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Topic cannot be blank")
        return v.strip()


class SuggestionResponse(BaseModel):
    suggestions: List[str]


@router.post("/suggestions", response_model=SuggestionResponse)
async def create_suggestions(
    request: SuggestionRequest,
    service: Annotated[SuggestionService, Depends(get_suggestion_service)],
    session: Annotated[AsyncSession, Depends(get_session_dep)],
) -> SuggestionResponse:
    try:
        suggestions = service.get_suggestions(request.topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    topic = Topic(title=request.topic.strip(), detail="")
    session.add(topic)
    await session.commit()
    await session.refresh(topic)

    for idx, content in enumerate(suggestions):
        session.add(
            Suggestion(topic_id=topic.id, content=content, position=idx)
        )
    await session.commit()

    return SuggestionResponse(suggestions=suggestions)

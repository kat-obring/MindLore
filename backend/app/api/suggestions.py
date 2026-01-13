from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from ..suggestions.service import SuggestionService
from .dependencies import get_suggestion_service

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
def create_suggestions(
    request: SuggestionRequest,
    service: Annotated[SuggestionService, Depends(get_suggestion_service)],
) -> SuggestionResponse:
    try:
        suggestions = service.get_suggestions(request.topic)
        return SuggestionResponse(suggestions=suggestions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

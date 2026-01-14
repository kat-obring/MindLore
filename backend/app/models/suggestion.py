from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class Suggestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.id")
    content: str
    position: int = 0

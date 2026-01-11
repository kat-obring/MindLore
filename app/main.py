import os
from datetime import datetime
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from sqlmodel import Field, Session, SQLModel, create_engine, select

DEFAULT_DATABASE_URL = "sqlite:///./app.db"
DEFAULT_STYLE_GUIDES_PATH = "docs/styleguides"
DEFAULT_MODEL = "gpt-4o-mini"


class Idea(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class IdeaCreate(SQLModel):
    title: str
    description: str = ""


class StyleGuide(SQLModel):
    name: str
    content: str


class OpenAIClient(Protocol):
    def generate_angles(
        self, *, idea_title: str, idea_description: str, style_guide_content: str
    ) -> list[str]:
        ...


class RealOpenAIClient:
    def __init__(self, api_key: str | None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate_angles(
        self, *, idea_title: str, idea_description: str, style_guide_content: str
    ) -> list[str]:
        prompt = (
            "Generate 3 distinct social media angles for this idea.\n"
            f"Idea: {idea_title}\n"
            f"Description: {idea_description}\n"
            f"Style guide:\n{style_guide_content}\n"
            "Return each angle as a short sentence prefixed with 'Option'."
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        text = completion.choices[0].message.content or ""
        # Split into lines, take first 3 non-empty
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines[:3] if len(lines) >= 3 else lines or ["Option 1", "Option 2", "Option 3"]


class StubOpenAIClient:
    def generate_angles(
        self, *, idea_title: str, idea_description: str, style_guide_content: str
    ) -> list[str]:
        base = idea_title or "idea"
        return [
            f"Option 1: {base} A",
            f"Option 2: {base} B",
            f"Option 3: {base} C",
        ]


def create_app(openai_client: OpenAIClient | None = None) -> FastAPI:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)

    if openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
        openai_client = (
            RealOpenAIClient(api_key=api_key, model=model) if api_key else StubOpenAIClient()
        )

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def get_session():
        with Session(engine) as session:
            yield session

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ideas", status_code=201)
    def create_idea(payload: IdeaCreate, session: Session = Depends(get_session)) -> Idea:
        idea = Idea(**payload.model_dump())
        session.add(idea)
        session.commit()
        session.refresh(idea)
        return idea

    @app.get("/ideas")
    def list_ideas(session: Session = Depends(get_session)) -> list[Idea]:
        results = session.exec(select(Idea).order_by(Idea.created_at, Idea.id)).all()
        return results

    @app.get("/style-guides")
    def list_style_guides() -> list[StyleGuide]:
        guides_dir = Path(os.getenv("STYLE_GUIDES_PATH", DEFAULT_STYLE_GUIDES_PATH))
        guides: list[StyleGuide] = []
        if guides_dir.exists():
            for path in sorted(guides_dir.glob("*.md")):
                guides.append(
                    StyleGuide(name=path.stem, content=path.read_text(encoding="utf-8"))
                )
        return guides

    @app.post("/ideas/{idea_id}/angles")
    def generate_angles(
        idea_id: int,
        payload: dict | None = None,
        session: Session = Depends(get_session),
    ) -> list[str]:
        idea = session.get(Idea, idea_id)
        if idea is None:
            return []

        payload = payload or {}
        style_guides = {guide.name: guide for guide in list_style_guides()}
        guide_name = payload.get("styleGuideName")
        guide = style_guides.get(guide_name) if guide_name else None

        style_content = guide.content if guide else ""

        return openai_client.generate_angles(
            idea_title=idea.title,
            idea_description=idea.description,
            style_guide_content=style_content,
        )

    return app


app = create_app()

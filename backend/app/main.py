from fastapi import FastAPI

from .api.health import router as health_router
from .core.config import get_settings
from .core.version import VERSION
from .prompts.repository import FilePromptRepository
from .suggestions.service import SuggestionService, FakeLLMClient

def get_prompt_repository() -> FilePromptRepository:
    return FilePromptRepository()

def get_llm_client() -> FakeLLMClient:
    return FakeLLMClient()

def get_suggestion_service() -> SuggestionService:
    return SuggestionService(get_prompt_repository(), get_llm_client())

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title="MindLore", version=VERSION)
    app.state.settings = settings
    app.state.version = VERSION

    # Dependency wiring placeholder for future routes.
    app.dependency_overrides[get_settings] = lambda: settings

    app.include_router(health_router)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host="0.0.0.0",
        port=get_settings().port,
        reload=True,
    )

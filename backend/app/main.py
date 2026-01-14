from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .api.dependencies import get_settings, _ensure_sqlite_dir
from .core.db import get_engine

from .api.health import router as health_router
from .api.suggestions import router as suggestions_router
from .api.topics import router as topics_router
from .core.version import VERSION


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        _ensure_sqlite_dir(settings.database_url)
        engine = get_engine(settings)
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        yield

    app = FastAPI(title="MindLore", version=VERSION, lifespan=lifespan)
    app.state.settings = settings
    app.state.version = VERSION

    # Dependency wiring placeholder for future routes.
    app.dependency_overrides[get_settings] = lambda: settings

    app.include_router(health_router)
    app.include_router(suggestions_router)
    app.include_router(topics_router)

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

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.version import VERSION


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

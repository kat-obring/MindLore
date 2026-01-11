import os

from backend.app.core.config import get_settings
from backend.app.main import create_app
from fastapi.testclient import TestClient


def _set_required_env() -> None:
    os.environ["OPENAI_API_KEY"] = "sk-health-123"


def _reset_settings_cache() -> None:
    get_settings.cache_clear()


def test_health_endpoint_returns_status_env_version(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _reset_settings_cache()
    _set_required_env()

    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["env"] == app.state.settings.app_env
    assert payload["version"] == app.state.version

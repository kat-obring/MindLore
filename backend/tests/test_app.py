import os

from backend.app.core.config import Settings, get_settings
from backend.app.core.version import VERSION
from backend.app.main import create_app
from fastapi import FastAPI


def _set_required_env() -> None:
    os.environ["OPENAI_API_KEY"] = "sk-app-123"


def _reset_settings_cache() -> None:
    get_settings.cache_clear()


def _get_openapi_payload(app_client) -> dict:
    response = app_client.get("/openapi.json")

    assert response.status_code == 200
    return response.json()


def test_create_app_attaches_settings(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _reset_settings_cache()
    _set_required_env()

    app = create_app()

    assert isinstance(app, FastAPI)
    assert isinstance(app.state.settings, Settings)
    assert app.state.settings.openai_api_key == "sk-app-123"


def test_create_app_sets_version_on_state(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _reset_settings_cache()
    _set_required_env()

    app = create_app()

    assert app.state.version == VERSION
    assert isinstance(VERSION, str) and VERSION


def test_docs_endpoint_serves_swagger_ui(app_client) -> None:
    response = app_client.get("/docs")

    assert response.status_code == 200
    assert "Swagger UI" in response.text


def test_openapi_schema_endpoint_returns_schema(app_client) -> None:
    payload = _get_openapi_payload(app_client)
    assert isinstance(payload, dict)
    assert "openapi" in payload
    assert "paths" in payload


def test_openapi_schema_includes_title_and_version(app_client) -> None:
    payload = _get_openapi_payload(app_client)
    assert payload["info"]["title"] == "MindLore"
    assert payload["info"]["version"] == app_client.app.state.version

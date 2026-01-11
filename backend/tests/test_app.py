import os

from fastapi import FastAPI

from backend.app.core.config import Settings, get_settings
from backend.app.core.version import VERSION
from backend.app.main import create_app


def _set_required_env() -> None:
    os.environ["OPENAI_API_KEY"] = "sk-app-123"


def _reset_settings_cache() -> None:
    get_settings.cache_clear()


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

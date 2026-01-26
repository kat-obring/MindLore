from pathlib import Path

import pytest
from backend.app.core.config import Settings
from pydantic import ValidationError


def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "APP_ENV",
        "CLAUDE_MODEL",
        "PORT",
        "CONTEXT_DIR",
        "CLAUDE_API_KEY",
        "DATABASE_URL",
    ):
        monkeypatch.delenv(key, raising=False)


def test_settings_load_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("CLAUDE_API_KEY", "sk-default-123")

    settings = Settings(_env_file=None)
    repo_root = Path(__file__).resolve().parents[2]

    assert settings.app_env == "dev"
    assert settings.claude_model == "claude-sonnet-4-20250514"
    assert settings.port == 8000
    assert str(settings.context_dir) == "data/context"
    assert settings.prompts_dir == repo_root / "prompts"


def test_settings_apply_env_overrides(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    monkeypatch.setenv("PORT", "9001")
    monkeypatch.setenv("PROMPTS_DIR", str(tmp_path))
    monkeypatch.setenv("CLAUDE_API_KEY", "sk-test-123")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./tmp/test.db")

    settings = Settings(_env_file=None)

    assert settings.app_env == "test"
    assert settings.claude_model == "claude-3-opus-20240229"
    assert settings.port == 9001
    assert settings.prompts_dir == tmp_path
    assert settings.claude_api_key == "sk-test-123"
    assert settings.database_url == "sqlite+aiosqlite:///./tmp/test.db"


def test_settings_require_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)

    monkeypatch.setenv("CLAUDE_API_KEY", "sk-required-123")

    settings = Settings(_env_file=None)

    assert settings.claude_api_key == "sk-required-123"


def test_settings_database_url_default(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("CLAUDE_API_KEY", "sk-default-123")

    settings = Settings(_env_file=None)

    assert settings.database_url == "sqlite+aiosqlite:///./var/mindlore.db"

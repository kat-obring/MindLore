from pathlib import Path

from backend.app.api.dependencies import get_prompt_repository
from backend.app.core.config import get_settings


def test_get_prompt_repository_uses_prompts_dir_env(
    monkeypatch, tmp_path: Path
) -> None:
    (tmp_path / "topics_first.md").write_text("env content", encoding="utf-8")
    monkeypatch.setenv("PROMPTS_DIR", str(tmp_path))
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    get_settings.cache_clear()

    repo = get_prompt_repository()

    assert repo.get_prompt("topics_first") == "env content"


def test_get_prompt_repository_defaults_to_repo_prompts_dir(monkeypatch) -> None:
    monkeypatch.delenv("PROMPTS_DIR", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    get_settings.cache_clear()

    repo = get_prompt_repository()

    assert "## Output format (required)" in repo.get_prompt("topics_first")

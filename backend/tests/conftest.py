import sys
import tempfile
from pathlib import Path

import pytest
from backend.app.core.config import get_settings
from backend.app.main import create_app
from fastapi.testclient import TestClient

# Ensure backend package is importable by adding project root ahead of default entries.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)


@pytest.fixture
def app_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    # Ensure settings reload with known env for deterministic tests.
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()
    tmp_dir = Path(tempfile.mkdtemp())
    db_path = tmp_dir / "test.db"
    monkeypatch.setenv("CLAUDE_API_KEY", "sk-test-123")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

    app = create_app()
    return TestClient(app)

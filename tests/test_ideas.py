from fastapi.testclient import TestClient

from app.main import create_app


def test_create_idea_persists(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/ideas", json={"title": "First idea", "description": "A test idea"}
    )

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == "First idea"
    assert created["description"] == "A test idea"

    list_response = client.get("/ideas")
    ideas = list_response.json()
    assert len(ideas) == 1
    assert ideas[0]["title"] == "First idea"


def test_options_ideas_allows_cors(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    client = TestClient(app)

    response = client.options(
        "/ideas",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in {
        "*",
        "http://localhost:3000",
    }
    methods = response.headers.get("access-control-allow-methods") or ""
    assert "POST" in methods


def test_create_idea_with_only_title_defaults_description(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    client = TestClient(app)

    response = client.post("/ideas", json={"title": "Just title"})

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == "Just title"
    assert created["description"] == ""

from fastapi.testclient import TestClient

from app.main import create_app


class StubOpenAIClient:
    def __init__(self) -> None:
        self.last_prompt = ""

    def generate_angles(
        self, *, idea_title: str, idea_description: str, style_guide_content: str
    ) -> list[str]:
        # record prompt parts for assertions
        self.last_prompt = f"{idea_title} | {idea_description} | {style_guide_content}"
        return [
            "Angle 1: A",
            "Angle 2: B",
            "Angle 3: C",
        ]


def test_generate_angles_uses_style_guide_and_returns_three_options(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'db.sqlite'}")
    guides_dir = tmp_path / "styleguides"
    guides_dir.mkdir()
    guide_content = "# Guide A\nTone: friendly"
    (guides_dir / "guide_a.md").write_text(guide_content, encoding="utf-8")
    monkeypatch.setenv("STYLE_GUIDES_PATH", str(guides_dir))

    stub_client = StubOpenAIClient()
    app = create_app(openai_client=stub_client)
    client = TestClient(app)

    idea = client.post(
        "/ideas", json={"title": "Launch feature", "description": "A new release"}
    ).json()

    response = client.post(
        f"/ideas/{idea['id']}/angles", json={"styleGuideName": "guide_a"}
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 3
    assert stub_client.last_prompt
    assert "Guide A" in stub_client.last_prompt
    assert "Launch feature" in stub_client.last_prompt


def test_generate_angles_allows_empty_body(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'db.sqlite'}")
    stub_client = StubOpenAIClient()
    app = create_app(openai_client=stub_client)
    client = TestClient(app)

    idea = client.post(
        "/ideas", json={"title": "Title only", "description": "Desc"}
    ).json()

    response = client.post(f"/ideas/{idea['id']}/angles")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 3

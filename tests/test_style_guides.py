from fastapi.testclient import TestClient

from app.main import create_app


def test_list_style_guides_reads_markdown_files(tmp_path, monkeypatch) -> None:
    guides_dir = tmp_path / "styleguides"
    guides_dir.mkdir()

    (guides_dir / "guide_a.md").write_text("# Guide A\nContent A", encoding="utf-8")
    (guides_dir / "guide_b.md").write_text("# Guide B\nContent B", encoding="utf-8")

    monkeypatch.setenv("STYLE_GUIDES_PATH", str(guides_dir))

    app = create_app()
    client = TestClient(app)

    response = client.get("/style-guides")
    assert response.status_code == 200

    guides = response.json()
    # Should return both guides with name and content, sorted by name
    assert [g["name"] for g in guides] == ["guide_a", "guide_b"]
    assert guides[0]["content"].startswith("# Guide A")
    assert guides[1]["content"].startswith("# Guide B")

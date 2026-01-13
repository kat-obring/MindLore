import pytest
from backend.app.context.store import ContextRecord, ContextStore


def test_list_contexts_returns_empty_for_empty_dir(tmp_path) -> None:
    store = ContextStore(root=tmp_path)

    assert store.list_contexts() == []


def test_list_contexts_reads_md_and_txt_files(tmp_path) -> None:
    (tmp_path / "topic-a.md").write_text("hello world", encoding="utf-8")
    (tmp_path / "topic-b.txt").write_text("another topic", encoding="utf-8")
    (tmp_path / "ignore.json").write_text("{}", encoding="utf-8")

    store = ContextStore(root=tmp_path)

    assert store.list_contexts() == [
        ContextRecord(slug="topic-a", content="hello world"),
        ContextRecord(slug="topic-b", content="another topic"),
    ]


def test_save_context_writes_and_overwrites_file(tmp_path) -> None:
    store = ContextStore(root=tmp_path)

    first = store.save_context("topic-a", "first content")

    path = tmp_path / "topic-a.md"
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "first content"
    assert first == ContextRecord(slug="topic-a", content="first content")
    assert store.list_contexts() == [first]

    second = store.save_context("topic-a", "updated content")

    assert path.read_text(encoding="utf-8") == "updated content"
    assert second == ContextRecord(slug="topic-a", content="updated content")


@pytest.mark.parametrize(
    "slug",
    [
        "../escape",
        "TopicA",
        "topic a",
        "topic/1",
        "topic_a",
        "",
    ],
)
def test_save_context_rejects_invalid_slug(slug, tmp_path) -> None:
    store = ContextStore(root=tmp_path)

    with pytest.raises(ValueError):
        store.save_context(slug, "content")


def test_list_contexts_handles_concurrent_deletion(tmp_path, monkeypatch) -> None:
    (tmp_path / "topic-a.md").write_text("hello", encoding="utf-8")
    store = ContextStore(root=tmp_path)

    # Mock Path.read_text to raise FileNotFoundError for topic-a.md
    from pathlib import Path

    original_read_text = Path.read_text

    def mock_read_text(self, *args, **kwargs):
        if self.stem == "topic-a":
            raise FileNotFoundError("Simulated deletion")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # Should not raise FileNotFoundError and should skip the missing file
    assert store.list_contexts() == []

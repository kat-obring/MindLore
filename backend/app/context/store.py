"""File-backed context store for markdown/text snippets.

- Stores files under ``data/context/`` (override via ``root``).
- Supports ``.md`` and ``.txt`` files.
- Slugs must be lowercase letters/numbers with hyphens (e.g., ``topic-1``).
"""
import re
from dataclasses import dataclass
from pathlib import Path


CONTEXT_DIR = Path("data/context")
SUPPORTED_EXTENSIONS = (".md", ".txt")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class ContextRecord:
    slug: str
    content: str


class ContextStore:
    def __init__(self, root: Path = CONTEXT_DIR) -> None:
        self.root = Path(root)

    def list_contexts(self) -> list[ContextRecord]:
        self.root.mkdir(parents=True, exist_ok=True)

        records: list[ContextRecord] = []
        for path in sorted(self.root.iterdir()):
            if not path.is_file() or path.suffix not in SUPPORTED_EXTENSIONS:
                continue
            if not SLUG_PATTERN.fullmatch(path.stem):
                continue
            content = path.read_text(encoding="utf-8")
            records.append(ContextRecord(slug=path.stem, content=content))

        return records

    def save_context(self, slug: str, content: str) -> ContextRecord:
        self.root.mkdir(parents=True, exist_ok=True)

        safe_slug = self._validate_slug(slug)
        path = self.root / f"{safe_slug}.md"
        path.write_text(content, encoding="utf-8")

        return ContextRecord(slug=safe_slug, content=content)

    def _validate_slug(self, slug: str) -> str:
        if not slug or not SLUG_PATTERN.fullmatch(slug):
            raise ValueError(
                "Slug must use lowercase letters, numbers, and hyphens only (e.g., topic-1)."
            )
        return slug

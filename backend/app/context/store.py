"""File-backed context store for markdown/text snippets.

- Stores files under ``data/context/`` (override via ``root``).
- Supports ``.md`` and ``.txt`` files.
- Slugs must be lowercase letters/numbers with hyphens (e.g., ``topic-1``).
"""

import re
from dataclasses import dataclass
from pathlib import Path

from ..core.config import get_settings

SUPPORTED_EXTENSIONS = (".md", ".txt")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class ContextRecord:
    slug: str
    content: str


class ContextStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or get_settings().context_dir

    def list_contexts(self) -> list[ContextRecord]:
        self._ensure_root()

        records: list[ContextRecord] = []
        for path in sorted(self.root.iterdir()):
            if not path.is_file():
                continue
            if path.suffix not in SUPPORTED_EXTENSIONS:
                continue
            slug = path.stem
            if not SLUG_PATTERN.fullmatch(slug):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except FileNotFoundError:
                continue
            records.append(ContextRecord(slug=slug, content=content))

        return records

    def save_context(self, slug: str, content: str) -> ContextRecord:
        self._ensure_root()

        safe_slug = self._validate_slug(slug)
        path = self.root / f"{safe_slug}.md"
        path.write_text(content, encoding="utf-8")

        return ContextRecord(slug=safe_slug, content=content)

    def _ensure_root(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def _validate_slug(self, slug: str) -> str:
        if slug and SLUG_PATTERN.fullmatch(slug):
            return slug
        raise ValueError(
            "Slug must use lowercase letters, numbers, and hyphens only "
            "(e.g., topic-1)."
        )

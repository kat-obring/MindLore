from backend.app.prompts.repository import FilePromptRepository


from pathlib import Path


def test_file_prompt_repository_loads_topics_first():
    # Resolve prompts directory relative to repo root to work from any cwd
    repo_root = Path(__file__).resolve().parents[2]
    prompts_dir = repo_root / "prompts"
    repo = FilePromptRepository(prompts_dir=prompts_dir)

    # When loading the 'topics_first' prompt
    content = repo.get_prompt("topics_first")

    # Then it should return the content of prompts/topics_first.md
    assert "## Output format (required)" in content
    assert "### Outline A:" in content

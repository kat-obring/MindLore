import pytest
import os
from backend.app.prompts.repository import FilePromptRepository

def test_file_prompt_repository_loads_topics_first():
    # Given a repository pointing to the prompts directory
    # In tests, we need to find where the prompts/ folder is relative to the test runner
    # The workspace root contains prompts/ and backend/
    # If running from backend/ directory, it is ../prompts
    repo = FilePromptRepository(prompts_dir="../prompts")
    
    # When loading the 'topics_first' prompt
    content = repo.get_prompt("topics_first")
    
    # Then it should return the content of prompts/topics_first.md
    assert "## Output format (required)" in content
    assert "### Outline A:" in content

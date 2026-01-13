import pytest
from app.suggestions.service import parse_suggestions

def test_parse_suggestions_extracts_exactly_three_outlines():
    # Given a sample LLM response with 3 outlines
    llm_response = """
Some introductory text that should be ignored.

### Outline A: The First Angle
* **Hook:** A hook for A.
* **Content:** Some content for A.

### Outline B: The Second Angle
* **Hook:** A hook for B.
* **Content:** Some content for B.

### Outline C: The Third Angle
* **Hook:** A hook for C.
* **Content:** Some content for C.

Some trailing text that should be ignored.
"""
    
    # When
    suggestions = parse_suggestions(llm_response)
    
    # Then
    assert len(suggestions) == 3
    assert suggestions[0].strip().startswith("### Outline A:")
    assert suggestions[1].strip().startswith("### Outline B:")
    assert suggestions[2].strip().startswith("### Outline C:")
    assert "The First Angle" in suggestions[0]
    assert "The Second Angle" in suggestions[1]
    assert "The Third Angle" in suggestions[2]

def test_parse_suggestions_raises_error_if_not_exactly_three():
    # Given a response with only 2 outlines
    llm_response = "### Outline A: One\n\n### Outline B: Two"
    
    # When / Then
    with pytest.raises(ValueError, match="Expected exactly 3 suggestions"):
        parse_suggestions(llm_response)

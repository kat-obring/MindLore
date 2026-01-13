from backend.app.prompts.repository import render_prompt

def test_render_prompt_includes_topic_and_content():
    # Given
    prompt_template = "System instructions here."
    topic = "Testing TDD in Python"
    
    # When
    final_prompt = render_prompt(prompt_template, topic)
    
    # Then
    assert prompt_template in final_prompt
    assert topic in final_prompt
    assert "Topic:" in final_prompt
    # Ensure topic is only included once
    assert final_prompt.count(topic) == 1

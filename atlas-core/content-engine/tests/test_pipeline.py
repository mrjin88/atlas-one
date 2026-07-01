import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import ContentPipeline


def test_pipeline_returns_structured_plan() -> None:
    pipeline = ContentPipeline()
    result = pipeline.run("A short documentary about forgotten cities")

    assert result.idea == "A short documentary about forgotten cities"
    assert len(result.research) == 1
    assert len(result.script) == 1
    assert len(result.image_prompts) == 1
    assert len(result.video_prompts) == 1
    assert len(result.seo) == 1
    assert len(result.publish_checklist) == 1
    assert result.research[0] == "[Mock AI response for: You are a research assistant. Research the following topic and generate a structured markdown document.\n\nTopic: A short documentary about forgotten cities\n\nInclude the following sections in your response:\n\n# Historical Context\n\n# Key Facts\n\n# Timeline\n\n# Interesting Details\n\n# Sources to Verify\n\nUse markdown formatting throughout.]"
    assert result.script[0] == "Draft a script for the idea: A short documentary about forgotten cities"
    assert result.image_prompts[0] == "Create image prompts for: A short documentary about forgotten cities"

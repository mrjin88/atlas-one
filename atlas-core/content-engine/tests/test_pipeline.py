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
    assert len(result.publish_checklist) == 10
    assert result.research[0]
    assert "forgotten cities" in result.research[0]
    assert "Historical Context" in result.research[0]
    assert "Key Facts" in result.research[0]
    assert result.script[0]
    assert "forgotten cities" in result.script[0]
    assert "Hook" in result.script[0]
    assert "Introduction" in result.script[0]
    assert "Story" in result.script[0]
    assert "Interesting Facts" in result.script[0]
    assert "Closing" in result.script[0]
    assert "Call To Action" in result.script[0]
    assert result.image_prompts[0]
    assert "forgotten cities" in result.image_prompts[0]
    assert "Thumbnail Concept" in result.image_prompts[0]
    assert "Reference Style" in result.image_prompts[0]

    assert result.video_prompts[0]
    assert "forgotten cities" in result.video_prompts[0]
    assert "Video Concept" in result.video_prompts[0]
    assert "Scene Breakdown" in result.video_prompts[0]

    assert result.seo[0]
    assert "forgotten cities" in result.seo[0]
    assert "Target Keywords" in result.seo[0]
    assert "Title Suggestions" in result.seo[0]

    assert result.publish_checklist[0]
    assert len(result.publish_checklist) == 10
    assert "Review and approve" in result.publish_checklist[0]
    assert "Monitor initial engagement" in result.publish_checklist[-1]

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class ContentPlan:
    """Structured output for a content pipeline run."""

    idea: str
    research: List[str] = field(default_factory=list)
    script: List[str] = field(default_factory=list)
    image_prompts: List[str] = field(default_factory=list)
    video_prompts: List[str] = field(default_factory=list)
    seo: List[str] = field(default_factory=list)
    publish_checklist: List[str] = field(default_factory=list)

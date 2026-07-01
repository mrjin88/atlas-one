from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List

from engine import ContentEngine
from models import ContentPlan


class PipelineResult(ContentPlan):
    """Structured content plan produced by the pipeline."""


class ContentPipeline:
    """Orchestrates the content pipeline by coordinating the engine."""

    def __init__(self, engine: ContentEngine | None = None) -> None:
        self.engine = engine or ContentEngine()

    def run(self, idea: str) -> PipelineResult:
        if not idea.strip():
            raise ValueError("Idea must not be empty")

        results = self.engine.run(idea)

        return PipelineResult(
            idea=idea,
            research=results.get("research", []),
            script=results.get("script", []),
            image_prompts=results.get("image_prompts", []),
            video_prompts=results.get("video_prompts", []),
            seo=results.get("seo", []),
            publish_checklist=results.get("publish_checklist", []),
        )

    def to_dict(self, plan: PipelineResult) -> dict[str, List[str] | str]:
        return asdict(plan)

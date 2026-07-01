from __future__ import annotations

from typing import List

from .base import Provider


class VideoPromptProvider(Provider):
    """Provides placeholder video prompt output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Create video prompts for: {idea}"]

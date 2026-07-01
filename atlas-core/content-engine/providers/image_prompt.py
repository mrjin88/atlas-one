from __future__ import annotations

from typing import List

from .base import Provider


class ImagePromptProvider(Provider):
    """Provides placeholder image prompt output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Create image prompts for: {idea}"]

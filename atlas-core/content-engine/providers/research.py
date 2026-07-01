from __future__ import annotations

from typing import List

from .base import Provider


class ResearchProvider(Provider):
    """Provides placeholder research output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Research the concept behind: {idea}"]

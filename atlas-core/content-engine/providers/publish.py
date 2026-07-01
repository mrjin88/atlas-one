from __future__ import annotations

from typing import List

from .base import Provider


class PublishProvider(Provider):
    """Provides placeholder publishing checklist output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Prepare publishing checklist for: {idea}"]

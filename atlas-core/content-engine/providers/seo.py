from __future__ import annotations

from typing import List

from .base import Provider


class SEOProvider(Provider):
    """Provides placeholder SEO output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Create SEO guidance for: {idea}"]

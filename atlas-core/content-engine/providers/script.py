from __future__ import annotations

from typing import List

from .base import Provider


class ScriptProvider(Provider):
    """Provides placeholder script output for an idea."""

    def generate(self, idea: str) -> List[str]:
        return [f"Draft a script for the idea: {idea}"]

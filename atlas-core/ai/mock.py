"""Mock AI provider for development and testing."""

from __future__ import annotations

from .base import AIProvider


class MockProvider(AIProvider):
    """A mock AI provider that returns predictable placeholder text.

    Useful for development, testing, and CI environments where
    a real AI model is not available.
    """

    def generate(self, prompt: str) -> str:
        return f"[Mock AI response for: {prompt}]"

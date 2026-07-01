from __future__ import annotations

import os
from typing import List, Optional

from ai.base import AIProvider
from ai.mock import MockProvider
from ai.providers.openai_provider import OpenAIProvider

from .base import Provider


_RESEARCH_PROMPT_TEMPLATE = """You are a research assistant. Research the following topic and generate a structured markdown document.

Topic: {idea}

Include the following sections in your response:

# Historical Context

# Key Facts

# Timeline

# Interesting Details

# Sources to Verify

Use markdown formatting throughout."""


class ResearchProvider(Provider):
    """AI-powered research provider.

    Uses an AIProvider to generate structured research markdown
    for a given idea. Falls back to MockProvider when no
    OPENAI_API_KEY is set.
    """

    def __init__(self, ai_provider: AIProvider | None = None) -> None:
        self._ai = ai_provider or self._default_ai()

    @staticmethod
    def _default_ai() -> AIProvider:
        if os.environ.get("OPENAI_API_KEY"):
            return OpenAIProvider()
        return MockProvider()

    def generate(self, idea: str) -> List[str]:
        prompt = _RESEARCH_PROMPT_TEMPLATE.format(idea=idea)
        content = self._ai.generate(prompt)
        return [content]

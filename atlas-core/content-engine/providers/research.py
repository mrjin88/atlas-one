from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from .base import Provider

# Ensure atlas-core is on sys.path so the ai module can be imported
_core_path = str(Path(__file__).resolve().parents[2])
if _core_path not in sys.path:
    sys.path.insert(0, _core_path)

from ai.base import AIProvider
from ai.mock import MockProvider
from ai.providers.openai_provider import OpenAIProvider


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

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

from prompt_loader import PromptLoader


class ScriptProvider(Provider):
    """AI-powered script provider.

    Uses an AIProvider to generate a structured script in markdown.
    Falls back to MockProvider when no OPENAI_API_KEY is set.
    """

    def __init__(
        self,
        ai_provider: AIProvider | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        self._ai = ai_provider or self._default_ai()
        self._loader = prompt_loader or PromptLoader()

    @staticmethod
    def _default_ai() -> AIProvider:
        if os.environ.get("OPENAI_API_KEY"):
            return OpenAIProvider()
        return MockProvider()

    def generate(self, idea: str) -> List[str]:
        prompt = self._loader.load("script", idea=idea)
        content = self._ai.generate(prompt)
        return [content]

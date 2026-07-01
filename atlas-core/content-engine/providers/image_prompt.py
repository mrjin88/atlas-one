from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from .base import Provider

_core_path = str(Path(__file__).resolve().parents[2])
if _core_path not in sys.path:
    sys.path.insert(0, _core_path)

from ai.base import AIProvider
from ai.mock import MockProvider
from ai.providers.openai_provider import OpenAIProvider

try:
    from ..prompt_loader import PromptLoader
except ImportError:
    from prompt_loader import PromptLoader


class ImagePromptProvider(Provider):
    """AI-powered image prompt provider."""

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
        prompt = self._loader.load("image_prompt", idea=idea)
        content = self._ai.generate(prompt)
        return [content]

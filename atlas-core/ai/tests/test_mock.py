"""Tests for the mock AI provider."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.mock import MockProvider
from ai.base import AIProvider


class TestMockProvider:
    """Unit tests for MockProvider."""

    def test_is_valid_ai_provider(self) -> None:
        provider = MockProvider()
        assert isinstance(provider, AIProvider)

    def test_generate_returns_placeholder(self) -> None:
        provider = MockProvider()
        result = provider.generate("What is Roman concrete?")
        assert result == "[Mock AI response for: What is Roman concrete?]"

    def test_generate_handles_empty_prompt(self) -> None:
        provider = MockProvider()
        result = provider.generate("")
        assert result == "[Mock AI response for: ]"

    def test_generate_handles_different_prompts(self) -> None:
        provider = MockProvider()
        result1 = provider.generate("Hello")
        result2 = provider.generate("World")
        assert result1 != result2
        assert "Hello" in result1
        assert "World" in result2

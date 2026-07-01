"""Tests for the AI provider registry."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.registry import AIProviderRegistry
from ai.mock import MockProvider


class TestAIProviderRegistry:
    """Unit tests for AIProviderRegistry."""

    def test_register_and_get(self) -> None:
        registry = AIProviderRegistry()
        registry.register("mock", MockProvider)
        assert registry.get("mock") is MockProvider

    def test_register_duplicate_raises(self) -> None:
        registry = AIProviderRegistry()
        registry.register("mock", MockProvider)
        with pytest.raises(ValueError):
            registry.register("mock", MockProvider)

    def test_get_nonexistent_raises(self) -> None:
        registry = AIProviderRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_list_returns_sorted_names(self) -> None:
        registry = AIProviderRegistry()
        registry.register("z", MockProvider)
        registry.register("a", MockProvider)
        assert registry.list() == ["a", "z"]

    def test_list_empty(self) -> None:
        registry = AIProviderRegistry()
        assert registry.list() == []

    def test_exists_returns_true(self) -> None:
        registry = AIProviderRegistry()
        registry.register("mock", MockProvider)
        assert registry.exists("mock") is True

    def test_exists_returns_false(self) -> None:
        registry = AIProviderRegistry()
        assert registry.exists("mock") is False

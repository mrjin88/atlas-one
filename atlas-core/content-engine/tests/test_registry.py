import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from providers.registry import ProviderRegistry
from providers.research import ResearchProvider
from providers.script import ScriptProvider


class TestProviderRegistry:
    """Unit tests for ProviderRegistry."""

    def test_register_and_get(self) -> None:
        registry = ProviderRegistry()
        registry.register("research", ResearchProvider)
        assert registry.get("research") is ResearchProvider

    def test_register_duplicate_raises(self) -> None:
        registry = ProviderRegistry()
        registry.register("research", ResearchProvider)
        try:
            registry.register("research", ResearchProvider)
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_exists_returns_true_for_registered(self) -> None:
        registry = ProviderRegistry()
        registry.register("script", ScriptProvider)
        assert registry.exists("script") is True

    def test_exists_returns_false_for_unregistered(self) -> None:
        registry = ProviderRegistry()
        assert registry.exists("unknown") is False

    def test_list_returns_sorted_names(self) -> None:
        registry = ProviderRegistry()
        registry.register("z_provider", ResearchProvider)
        registry.register("a_provider", ScriptProvider)
        assert registry.list() == ["a_provider", "z_provider"]

    def test_list_empty(self) -> None:
        registry = ProviderRegistry()
        assert registry.list() == []

    def test_unregister_removes_provider(self) -> None:
        registry = ProviderRegistry()
        registry.register("research", ResearchProvider)
        registry.unregister("research")
        assert registry.exists("research") is False
        assert registry.list() == []

    def test_unregister_nonexistent_raises(self) -> None:
        registry = ProviderRegistry()
        try:
            registry.unregister("nonexistent")
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_get_nonexistent_raises(self) -> None:
        registry = ProviderRegistry()
        try:
            registry.get("nonexistent")
            assert False, "Expected KeyError"
        except KeyError:
            pass

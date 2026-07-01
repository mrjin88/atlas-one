from __future__ import annotations

from typing import Dict, List

from providers.registry import ProviderRegistry


class ContentEngine:
    """Orchestrator that dispatches work to providers via a registry.

    The engine does not know about concrete providers. All provider
    resolution is delegated to the ProviderRegistry.
    """

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
    ) -> None:
        self._registry = registry or ProviderRegistry()

    def run(self, idea: str) -> Dict[str, List[str]]:
        results: Dict[str, List[str]] = {}
        for name in self._registry.list():
            provider_cls = self._registry.get(name)
            provider = provider_cls()
            results[name] = provider.generate(idea)
        return results

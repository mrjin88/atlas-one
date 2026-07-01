from __future__ import annotations

from typing import Dict, List, Type

from providers.base import Provider


class ProviderRegistry:
    """Single source of truth for all content pipeline providers.

    Providers are registered by name and can be retrieved,
    listed, checked, and unregistered at runtime.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Provider]] = {}

    def register(self, name: str, provider: Type[Provider]) -> None:
        """Register a provider under a unique name."""
        if name in self._registry:
            raise ValueError(
                f"Provider '{name}' is already registered."
            )
        self._registry[name] = provider

    def get(self, name: str) -> Type[Provider]:
        """Retrieve a provider class by name."""
        if name not in self._registry:
            raise KeyError(f"Provider '{name}' is not registered.")
        return self._registry[name]

    def list(self) -> List[str]:
        """Return a sorted list of registered provider names."""
        return sorted(self._registry.keys())

    def exists(self, name: str) -> bool:
        """Check whether a provider is registered."""
        return name in self._registry

    def unregister(self, name: str) -> None:
        """Remove a registered provider by name."""
        if name not in self._registry:
            raise KeyError(f"Provider '{name}' is not registered.")
        del self._registry[name]

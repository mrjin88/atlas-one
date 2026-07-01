"""Registry for AI provider implementations."""

from __future__ import annotations

from typing import Dict, List, Type

from .base import AIProvider


class AIProviderRegistry:
    """Registry of available AI provider implementations.

    Providers are registered by a short name and can be
    retrieved and listed at runtime.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Type[AIProvider]] = {}

    def register(self, name: str, provider: Type[AIProvider]) -> None:
        """Register an AI provider under a unique name."""
        if name in self._registry:
            raise ValueError(
                f"AI provider '{name}' is already registered."
            )
        self._registry[name] = provider

    def get(self, name: str) -> Type[AIProvider]:
        """Retrieve an AI provider class by name."""
        if name not in self._registry:
            raise KeyError(f"AI provider '{name}' is not registered.")
        return self._registry[name]

    def list(self) -> List[str]:
        """Return a sorted list of registered provider names."""
        return sorted(self._registry.keys())

    def exists(self, name: str) -> bool:
        """Check whether an AI provider is registered."""
        return name in self._registry

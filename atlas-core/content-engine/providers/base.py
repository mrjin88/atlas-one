from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """Base interface for content pipeline providers."""

    @abstractmethod
    def generate(self, idea: str) -> Any:
        """Generate a provider-specific output for an idea."""
        raise NotImplementedError

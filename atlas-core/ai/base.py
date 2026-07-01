"""Abstract base class for AI providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract interface for AI model providers.

    Every AI provider must implement the ``generate`` method,
    which accepts a prompt and returns a textual response.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Send a prompt to the AI model and return the response.

        Args:
            prompt: The input text prompt.

        Returns:
            The generated text response.
        """
        raise NotImplementedError

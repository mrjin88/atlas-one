"""OpenAI provider implementation."""

from __future__ import annotations

import os
from typing import Any, Dict

from openai import APIError, OpenAI

from ai.base import AIProvider


class MissingAPIKeyError(Exception):
    """Raised when the OPENAI_API_KEY environment variable is not set."""


class OpenAIProviderError(Exception):
    """Raised when the OpenAI API returns an error."""


class OpenAIProvider(AIProvider):
    """AI provider backed by the OpenAI API.

    Reads the API key from the ``OPENAI_API_KEY`` environment variable.

    Configurable parameters:
        model: The OpenAI model identifier (default: ``gpt-4o``).
        temperature: Sampling temperature (default: ``0.7``).
        max_tokens: Maximum tokens in the response (default: ``1024``).
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        client: OpenAI | None = None,
    ) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key and client is None:
            raise MissingAPIKeyError(
                "OPENAI_API_KEY environment variable is not set."
            )
        self._client = client or OpenAI(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        """Send a prompt to OpenAI and return the response text."""
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
        except APIError as exc:
            raise OpenAIProviderError(
                f"OpenAI API error: {exc}"
            ) from exc

        choice = response.choices[0]
        content = choice.message.content
        return content or ""

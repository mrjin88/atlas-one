"""Tests for the OpenAI provider."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from openai import APIError as OpenAIAPIError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import ai.providers.openai_provider as op  # noqa: E402


class MockChoice:
    def __init__(self, content: str) -> None:
        self.message = MagicMock(content=content)


class MockResponse:
    def __init__(self, content: str) -> None:
        self.choices = [MockChoice(content)]


class TestOpenAIProvider:
    """Unit tests for OpenAIProvider (mocked SDK, no real API calls)."""

    def test_missing_api_key_raises_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(op.MissingAPIKeyError):
                op.OpenAIProvider(model="gpt-4o-mini")

    def test_generate_returns_content(self) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse(
            "Hello from OpenAI!"
        )
        provider = op.OpenAIProvider(
            model="gpt-4o-mini",
            client=mock_client,
        )
        result = provider.generate("Say hello")
        assert result == "Hello from OpenAI!"

    def test_generate_sends_correct_messages(self) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse("")
        provider = op.OpenAIProvider(
            model="gpt-4o-mini",
            client=mock_client,
        )
        provider.generate("What is AI?")
        mock_client.chat.completions.create.assert_called_once()
        _, kwargs = mock_client.chat.completions.create.call_args
        assert kwargs["messages"] == [
            {"role": "user", "content": "What is AI?"}
        ]

    def test_generate_uses_configured_model(self) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse("")
        provider = op.OpenAIProvider(
            model="gpt-4o-mini",
            temperature=0.5,
            max_tokens=512,
            client=mock_client,
        )
        provider.generate("Test")
        _, kwargs = mock_client.chat.completions.create.call_args
        assert kwargs["model"] == "gpt-4o-mini"
        assert kwargs["temperature"] == 0.5
        assert kwargs["max_tokens"] == 512

    def test_generate_raises_openai_api_error(self) -> None:
        mock_client = MagicMock()
        import httpx

        mock_client.chat.completions.create.side_effect = OpenAIAPIError(
            message="API failure",
            request=httpx.Request("POST", "https://api.openai.com"),
            body=None,
        )
        with pytest.raises(op.OpenAIAPIError):
            provider = op.OpenAIProvider(
                model="gpt-4o-mini",
                client=mock_client,
            )
            provider.generate("Test")

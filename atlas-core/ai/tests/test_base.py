"""Tests for the AI provider base class."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.base import AIProvider


class TestAIProvider:
    """Unit tests for the AIProvider abstract interface."""

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            AIProvider()  # type: ignore[abstract]

    def test_concrete_subclass_must_implement_generate(self) -> None:
        with pytest.raises(TypeError):

            class Incomplete(AIProvider):
                pass

            Incomplete()

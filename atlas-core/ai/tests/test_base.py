"""Tests for the AI provider base class."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.base import AIProvider


class TestAIProvider:
    """Unit tests for the AIProvider abstract interface."""

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        try:
            AIProvider()  # type: ignore[abstract]
            assert False, "Expected TypeError"
        except TypeError:
            pass

    def test_concrete_subclass_must_implement_generate(self) -> None:
        try:
            class Incomplete(AIProvider):
                pass
            Incomplete()
            assert False, "Expected TypeError"
        except TypeError:
            pass

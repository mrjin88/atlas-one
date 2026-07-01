"""Tests for the prompt template loader."""

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prompt_loader import PromptLoader, PromptNotFoundError, PromptVariableError


class TestPromptLoader:
    """Unit tests for PromptLoader."""

    def test_load_returns_template_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            prompt_dir = Path(tmpdir)
            prompt_dir.joinpath("test.md").write_text(
                "Research topic: {idea}", encoding="utf-8",
            )
            loader = PromptLoader(prompts_dir=prompt_dir)
            result = loader.load("test", idea="Roman concrete")
            assert result == "Research topic: Roman concrete"

    def test_load_raises_error_for_missing_template(self) -> None:
        loader = PromptLoader(prompts_dir=Path("/nonexistent"))
        with pytest.raises(PromptNotFoundError):
            loader.load("missing")

    def test_load_raises_error_for_missing_variable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            prompt_dir = Path(tmpdir)
            prompt_dir.joinpath("bad.md").write_text(
                "Topic: {idea}", encoding="utf-8",
            )
            loader = PromptLoader(prompts_dir=prompt_dir)
            with pytest.raises(PromptVariableError):
                loader.load("bad")

    def test_load_with_multiple_variables(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            prompt_dir = Path(tmpdir)
            prompt_dir.joinpath("multi.md").write_text(
                "A: {a}, B: {b}", encoding="utf-8",
            )
            loader = PromptLoader(prompts_dir=prompt_dir)
            result = loader.load("multi", a="1", b="2")
            assert result == "A: 1, B: 2"

    def test_default_prompts_dir_resolves_correctly(self) -> None:
        loader = PromptLoader()
        expected = (
            Path(__file__).resolve().parents[2] / "prompts"
        )
        assert loader._prompts_dir == expected

    def test_load_real_research_template(self) -> None:
        loader = PromptLoader()
        result = loader.load("research", idea="Roman concrete")
        assert "Roman concrete" in result
        assert "Historical Context" in result
        assert "Key Facts" in result
        assert "Timeline" in result
        assert "Interesting Details" in result
        assert "Sources to Verify" in result

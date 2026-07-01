"""Tests for the AI-powered research provider."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generator import ContentPackageGenerator
from pipeline import ContentPipeline
from prompt_loader import PromptLoader

from providers.research import ResearchProvider


class TestResearchProvider:
    """Tests for the AI-powered ResearchProvider."""

    def test_uses_ai_provider(self) -> None:
        mock_ai = MagicMock()
        mock_ai.generate.return_value = "# Test Research\n\nSome content."
        provider = ResearchProvider(ai_provider=mock_ai)
        result = provider.generate("Test topic")
        assert result == ["# Test Research\n\nSome content."]

    def test_prompt_contains_topic(self) -> None:
        mock_ai = MagicMock()
        mock_ai.generate.return_value = "# Mock"
        provider = ResearchProvider(ai_provider=mock_ai)
        provider.generate("Ancient Rome")
        prompt = mock_ai.generate.call_args[0][0]
        assert "Ancient Rome" in prompt
        assert "Historical Context" in prompt
        assert "Key Facts" in prompt
        assert "Timeline" in prompt
        assert "Interesting Details" in prompt
        assert "Sources to Verify" in prompt

    def test_generator_writes_raw_markdown_directly(self) -> None:
        """Verify that raw markdown content from the AI provider is written
        without the list wrapper in the generated file."""
        mock_ai = MagicMock()
        mock_ai.generate.return_value = (
            "# Historical Context\n\nContent here.\n\n"
            "# Key Facts\n\n- Fact one\n- Fact two"
        )
        provider = ResearchProvider(ai_provider=mock_ai)
        result = provider.generate("Test")

        plan = ContentPipeline().run("Test")
        plan.research = result

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)
            content = Path(files["research"]).read_text(encoding="utf-8")
            assert content.startswith("# Historical Context")
            assert "Content here." in content
            assert "Fact one" in content

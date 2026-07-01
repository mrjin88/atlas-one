import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli import build_parser, main


class TestCLI:
    """Tests for the Content Engine CLI."""

    def test_parser_accepts_idea(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--idea", "Test concept"])
        assert args.idea == "Test concept"

    def test_parser_requires_idea(self) -> None:
        parser = build_parser()
        try:
            parser.parse_args([])
            assert False, "Expected SystemExit"
        except SystemExit:
            pass

    def test_main_returns_zero_and_valid_json(self) -> None:
        exit_code = main(["--idea", "Roman concrete"])
        assert exit_code == 0

    def test_main_returns_one_for_empty_idea(self) -> None:
        exit_code = main(["--idea", ""])
        assert exit_code == 1

    def test_main_returns_one_for_whitespace_idea(self) -> None:
        exit_code = main(["--idea", "   "])
        assert exit_code == 1

    def test_output_is_valid_json(self, capsys) -> None:
        main(["--idea", "Lost civilizations"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["idea"] == "Lost civilizations"
        assert isinstance(data["research"], list)
        assert isinstance(data["script"], list)
        assert isinstance(data["image_prompts"], list)
        assert isinstance(data["video_prompts"], list)
        assert isinstance(data["seo"], list)
        assert isinstance(data["publish_checklist"], list)

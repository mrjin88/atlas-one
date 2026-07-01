"""Tests for the batch runner."""

import csv
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "atlas-core" / "content-engine"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "atlas-core"))

from batch_runner import load_topics, slugify, write_csv, write_summary


class TestBatchRunner:
    """Unit tests for batch runner utilities."""

    def test_slugify_basic(self) -> None:
        assert slugify("Roman concrete") == "roman-concrete"

    def test_slugify_special_chars(self) -> None:
        assert slugify("What is AI?") == "what-is-ai"

    def test_slugify_multiple_spaces(self) -> None:
        assert slugify("  The   Library   ") == "the-library"

    def test_load_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "topics.yaml"
            data = {"topics": ["A", "B", "C"]}
            path.write_text(yaml.dump(data), encoding="utf-8")
            topics = load_topics(path)
            assert topics == ["A", "B", "C"]

    def test_load_topics_empty_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "empty.yaml"
            path.write_text(yaml.dump({"topics": []}), encoding="utf-8")
            with pytest.raises(SystemExit):
                load_topics(path)

    def test_write_csv_creates_file(self) -> None:
        records = [
            {"Topic": "Test", "Research Score": 1, "Script Score": 1,
             "Image Score": 1, "Video Score": 1, "SEO Score": 1,
             "Overall Score": 5, "Reviewer Notes": ""},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "eval.csv"
            write_csv(records, path)
            assert path.exists()
            with path.open(encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) == 1
                assert rows[0]["Topic"] == "Test"

    def test_write_summary_creates_file(self) -> None:
        records = [
            {"Topic": "Test", "Overall Score": 5, "Reviewer Notes": ""},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_base = Path(tmpdir)
            path = Path(tmpdir) / "summary.md"
            write_summary(records, total=1, failed=0,
                          output_base=out_base, path=path)
            assert path.exists()
            content = path.read_text(encoding="utf-8")
            assert "Alpha Validation Summary" in content
            assert "Total topics" in content
            assert "Successful" in content
            assert "Success rate" in content
            assert "100.0%" in content

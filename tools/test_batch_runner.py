"""Tests for the batch runner."""

import csv
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "atlas-core" / "content-engine"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "atlas-core"))

from batch_runner import (
    load_topics,
    slugify,
    write_csv,
    write_manifest,
    write_summary,
    write_topics_list,
)


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

    def test_write_csv_has_headers_only(self) -> None:
        records = [
            {"Topic": "Test", "Research Score": "", "Script Score": "",
             "Image Score": "", "Video Score": "", "SEO Score": "",
             "Overall Score": "", "Reviewer Notes": ""},
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
                assert rows[0]["Research Score"] == ""

    def test_write_csv_empty_scores(self) -> None:
        records = [
            {"Topic": "A", "Research Score": "", "Script Score": "",
             "Image Score": "", "Video Score": "", "SEO Score": "",
             "Overall Score": "", "Reviewer Notes": ""},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "eval.csv"
            write_csv(records, path)
            content = path.read_text(encoding="utf-8")
            assert "Topic," in content
            assert "Overall Score" in content
            # Score columns should be empty
            lines = content.strip().split("\n")
            values = lines[1].split(",")
            assert values[1:] == [""] * 7

    def test_write_summary_creates_file(self) -> None:
        records = [
            {"Topic": "Test", "Overall Score": "", "Reviewer Notes": ""},
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

    def test_write_manifest_creates_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.json"
            write_manifest(
                run_id="run_test",
                topic_count=5,
                success_count=4,
                failure_count=1,
                duration_seconds=12.5,
                path=path,
            )
            assert path.exists()
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data["run_id"] == "run_test"
            assert data["topic_count"] == 5
            assert data["success_count"] == 4
            assert data["failure_count"] == 1
            assert data["duration_seconds"] == 12.5
            assert "git_commit" in data
            assert "prompt_version" in data

    def test_write_topics_list(self) -> None:
        topics = ["A", "B", "C"]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "topics.txt"
            write_topics_list(topics, path)
            content = path.read_text(encoding="utf-8").strip().split("\n")
            assert content == ["A", "B", "C"]

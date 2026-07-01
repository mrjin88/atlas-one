"""Batch runner for Atlas ONE content package generation.

Usage:
    python tools/batch_runner.py
    python tools/batch_runner.py --topics topics.yaml --output-dir projects/lost-archive/content
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

# Add atlas-core and content-engine to sys.path
_core = str(Path(__file__).resolve().parent.parent / "atlas-core")
_engine = str(Path(__file__).resolve().parent.parent / "atlas-core" / "content-engine")
for _p in [_core, _engine]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from pipeline import ContentPipeline  # noqa: E402
from generator import ContentPackageGenerator  # noqa: E402


def slugify(text: str) -> str:
    """Convert a topic string into a filesystem-safe slug."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s


def load_topics(path: str | Path) -> List[str]:
    """Load topics from a YAML file."""
    raw = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    topics = data.get("topics", [])
    if not topics:
        print("Error: No topics found in YAML file.", file=sys.stderr)
        sys.exit(1)
    return topics


def run_batch(
    topics: List[str],
    output_base: Path,
) -> List[Dict[str, str | int]]:
    """Run the content pipeline for each topic and return evaluation records."""
    pipeline = ContentPipeline()
    records: List[Dict[str, str | int]] = []
    failed = 0

    for idx, topic in enumerate(topics, start=1):
        slug = slugify(topic)
        out_dir = output_base / slug
        print(f"[{idx}/{len(topics)}] Processing: {topic}")

        try:
            plan = pipeline.run(topic)
            generator = ContentPackageGenerator(out_dir)
            files = generator.generate(plan)

            research_score = 1 if files.get("research") else 0
            script_score = 1 if files.get("script") else 0
            image_score = 1 if files.get("image_prompts") else 0
            video_score = 1 if files.get("video_prompts") else 0
            seo_score = 1 if files.get("seo") else 0

            overall = research_score + script_score + image_score + video_score + seo_score
            notes = ""

            print(f"  -> {len(files)} files generated in {out_dir}")
        except Exception as exc:
            print(f"  -> FAILED: {exc}")
            research_score = 0
            script_score = 0
            image_score = 0
            video_score = 0
            seo_score = 0
            overall = 0
            notes = str(exc)
            failed += 1

        records.append({
            "Topic": topic,
            "Research Score": research_score,
            "Script Score": script_score,
            "Image Score": image_score,
            "Video Score": video_score,
            "SEO Score": seo_score,
            "Overall Score": overall,
            "Reviewer Notes": notes,
        })

    print(f"\nBatch complete. {len(topics) - failed}/{len(topics)} succeeded.")
    return records


def write_csv(records: List[Dict[str, str | int]], path: Path) -> None:
    """Write evaluation records to a CSV file."""
    fieldnames = [
        "Topic",
        "Research Score",
        "Script Score",
        "Image Score",
        "Video Score",
        "SEO Score",
        "Overall Score",
        "Reviewer Notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"Evaluation CSV written to: {path}")


def write_summary(
    records: List[Dict[str, str | int]],
    total: int,
    failed: int,
    output_base: Path,
    path: Path,
) -> None:
    """Write a summary report in Markdown."""
    success = total - failed
    success_rate = (success / total * 100) if total > 0 else 0.0

    lines = [
        "# Alpha Validation Summary",
        "",
        f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- **Total topics:** {total}",
        f"- **Successful:** {success}",
        f"- **Failed:** {failed}",
        f"- **Success rate:** {success_rate:.1f}%",
        "",
        "## Output Directories",
        "",
    ]

    for record in records:
        topic = record["Topic"]
        slug = slugify(str(topic))
        out_path = output_base / slug
        lines.append(f"- [{topic}]({out_path}) - Score: {record['Overall Score']}/5")

    failed_records = [r for r in records if r["Overall Score"] == 0]
    if failed_records:
        lines.extend(["", "## Failed Generations", ""])
        for r in failed_records:
            lines.append(f"- {r['Topic']}: {r['Reviewer Notes']}")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary report written to: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Atlas ONE batch runner — generate content packages for multiple topics.",
    )
    parser.add_argument(
        "--topics",
        type=str,
        default=str(Path(__file__).resolve().parent / "topics.yaml"),
        help="Path to the topics YAML file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(
            Path(__file__).resolve().parent.parent
            / "projects" / "lost-archive" / "content"
        ),
        help="Base output directory for content packages.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    topics_path = Path(args.topics)
    output_base = Path(args.output_dir)

    topics = load_topics(topics_path)
    print(f"Loaded {len(topics)} topics from: {topics_path}")

    records = run_batch(topics, output_base)
    total = len(records)
    failed = sum(1 for r in records if r["Overall Score"] == 0)

    csv_path = Path(__file__).resolve().parent / "evaluation.csv"
    write_csv(records, csv_path)

    summary_path = Path(__file__).resolve().parent / "summary.md"
    write_summary(records, total, failed, output_base, summary_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())

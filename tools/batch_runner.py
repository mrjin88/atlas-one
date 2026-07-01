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
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import yaml

# Add atlas-core and content-engine to sys.path
_core = str(Path(__file__).resolve().parent.parent / "atlas-core")
_engine = str(Path(__file__).resolve().parent.parent / "atlas-core" / "content-engine")
for _p in [_core, _engine]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from pipeline import ContentPipeline  # noqa: E402
from generator import ContentPackageGenerator  # noqa: E402


_PROMPT_VERSION = "1.0.0"


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


def get_git_commit() -> str:
    """Return the current short Git commit hash, or 'unknown'."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=Path(__file__).resolve().parent.parent,
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def run_batch(
    topics: List[str],
    output_base: Path,
) -> tuple[List[Dict[str, str | int]], int]:
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
            generator.generate(plan)
            notes = ""
            print(f"  -> Files generated in {out_dir}")
        except Exception as exc:
            print(f"  -> FAILED: {exc}")
            notes = str(exc)
            failed += 1

        records.append({
            "Topic": topic,
            "Research Score": "",
            "Script Score": "",
            "Image Score": "",
            "Video Score": "",
            "SEO Score": "",
            "Overall Score": "",
            "Reviewer Notes": notes,
        })

    print(f"\nBatch complete. {len(topics) - failed}/{len(topics)} succeeded.")
    return records, failed


def write_csv(records: List[Dict[str, str | int]], path: Path) -> None:
    """Write evaluation CSV with headers and topic rows only."""
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
        lines.append(f"- [{topic}]({out_path})")

    failed_records = [r for r in records if r["Reviewer Notes"]]
    if failed_records:
        lines.extend(["", "## Failed Generations", ""])
        for r in failed_records:
            lines.append(f"- {r['Topic']}: {r['Reviewer Notes']}")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary report written to: {path}")


def write_manifest(
    run_id: str,
    topic_count: int,
    success_count: int,
    failure_count: int,
    duration_seconds: float,
    path: Path,
) -> None:
    """Write a run manifest as JSON."""
    manifest = {
        "run_id": run_id,
        "git_commit": get_git_commit(),
        "prompt_version": _PROMPT_VERSION,
        "topic_count": topic_count,
        "success_count": success_count,
        "failure_count": failure_count,
        "duration_seconds": round(duration_seconds, 2),
    }
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    print(f"Manifest written to: {path}")


def write_topics_list(topics: List[str], path: Path) -> None:
    """Write a plain-text list of topics."""
    path.write_text("\n".join(topics) + "\n", encoding="utf-8")
    print(f"Topics list written to: {path}")


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
    parser.add_argument(
        "--run-dir",
        type=str,
        default=None,
        help="Override run output directory (default: runs/<timestamp>/).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    start = time.time()
    parser = build_parser()
    args = parser.parse_args(argv)

    topics_path = Path(args.topics)
    output_base = Path(args.output_dir)

    topics = load_topics(topics_path)
    print(f"Loaded {len(topics)} topics from: {topics_path}")

    records, failed = run_batch(topics, output_base)
    total = len(records)
    success = total - failed

    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{timestamp}"
    tools_dir = Path(__file__).resolve().parent

    if args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        run_dir = tools_dir / "runs" / timestamp

    run_dir.mkdir(parents=True, exist_ok=True)

    csv_path = run_dir / "evaluation.csv"
    write_csv(records, csv_path)

    summary_path = run_dir / "summary.md"
    write_summary(records, total, failed, output_base, summary_path)

    topics_list_path = run_dir / "generated_topics.txt"
    write_topics_list(topics, topics_list_path)

    elapsed = time.time() - start
    manifest_path = run_dir / "manifest.json"
    write_manifest(run_id, total, success, failed, elapsed, manifest_path)

    print(f"\nAll run artifacts saved in: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

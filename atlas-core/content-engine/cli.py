"""Command-line interface for the Content Engine.

Usage:
    python cli.py --idea "Your idea here"
"""

from __future__ import annotations

import argparse
import json
import sys

try:
    from .pipeline import ContentPipeline
except ImportError:
    from pipeline import ContentPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Atlas ONE Content Engine — transform an idea into "
                    "a structured content plan.",
    )
    parser.add_argument(
        "--idea",
        type=str,
        required=True,
        help="The content idea to process.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    idea = args.idea.strip()
    if not idea:
        print("Error: --idea must not be empty.", file=sys.stderr)
        return 1

    pipeline = ContentPipeline()
    plan = pipeline.run(idea)
    output = json.dumps(pipeline.to_dict(plan), indent=2, ensure_ascii=False)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

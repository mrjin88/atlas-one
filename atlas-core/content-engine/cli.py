"""Command-line interface for the Content Engine.

Usage:
    python cli.py --idea "Your idea here"
    python cli.py --idea "Roman concrete" --output projects/lost-archive/content/LA-0001
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from .generator import ContentPackageGenerator
    from .pipeline import ContentPipeline
except ImportError:
    from generator import ContentPackageGenerator
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
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional output directory for generated content files.",
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

    output_path = args.output

    if output_path:
        generator = ContentPackageGenerator(output_path)
        files = generator.generate(plan)
        print(f"Generated {len(files)} files in: {Path(output_path).resolve()}")
        for section, filepath in sorted(files.items()):
            print(f"  {section}: {filepath}")
    else:
        out = json.dumps(pipeline.to_dict(plan), indent=2, ensure_ascii=False)
        print(out)

    return 0


if __name__ == "__main__":
    sys.exit(main())

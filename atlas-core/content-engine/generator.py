"""Content package generator — writes pipeline output to disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

try:
    from .pipeline import PipelineResult
except ImportError:
    from pipeline import PipelineResult


def _write_markdown(path: Path, title: str, items: List[str]) -> None:
    lines = [f"# {title}", ""]
    for item in items:
        lines.append(f"- {item}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_seo_json(path: Path, items: List[str]) -> None:
    data = {"seo_guidance": items}
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8",
    )


_SECTION_MAP: Dict[str, tuple[str, str, str]] = {
    "research": ("research.md", "Research Notes", "markdown"),
    "script": ("script.md", "Script Outline", "markdown"),
    "image_prompts": ("image_prompts.md", "Image Prompts", "markdown"),
    "video_prompts": ("video_prompts.md", "Video Prompts", "markdown"),
    "seo": ("seo.json", "", "json"),
    "publish_checklist": (
        "publish_checklist.md", "Publishing Checklist", "markdown",
    ),
}


class ContentPackageGenerator:
    """Writes a structured content package to disk."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    def generate(self, plan: PipelineResult) -> Dict[str, str]:
        """Generate all content files and return a map of section to file path.

        Returns:
            A dictionary mapping each section name to its generated file path.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        generated: Dict[str, str] = {}

        data = {
            "research": plan.research,
            "script": plan.script,
            "image_prompts": plan.image_prompts,
            "video_prompts": plan.video_prompts,
            "seo": plan.seo,
            "publish_checklist": plan.publish_checklist,
        }

        for section, items in data.items():
            filename, title, fmt = _SECTION_MAP[section]
            filepath = self.output_dir / filename

            if fmt == "json":
                _write_seo_json(filepath, items)
            else:
                _write_markdown(filepath, title, items)

            generated[section] = str(filepath.resolve())

        return generated

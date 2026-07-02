#!/usr/bin/env python3
"""
Atlas ONE Video Builder

Reads shots.yaml and exports production-ready prompt batches.
"""

from pathlib import Path
import csv
import json
import yaml

PROJECT_ROOT = Path.cwd()
SHOTS_FILE = PROJECT_ROOT / "shots.yaml"
OUT_DIR = PROJECT_ROOT / "exports" / "archive"


def load_shots():
    if not SHOTS_FILE.exists():
        raise FileNotFoundError(f"Missing {SHOTS_FILE}")
    with SHOTS_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def export_image_prompts(data):
    path = OUT_DIR / "image_prompt_batch.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "image_prompt", "negative_prompt", "output_path"])
        writer.writeheader()
        for shot in data["shots"]:
            writer.writerow({
                "id": shot["id"],
                "title": shot["title"],
                "image_prompt": shot["image_prompt"],
                "negative_prompt": shot["negative_prompt"],
                "output_path": shot["output"]["image_path"],
            })
    return path


def export_video_prompts(data):
    path = OUT_DIR / "video_prompt_batch.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "video_prompt", "reference_image", "output_path"])
        writer.writeheader()
        for shot in data["shots"]:
            writer.writerow({
                "id": shot["id"],
                "title": shot["title"],
                "video_prompt": shot["video_prompt"],
                "reference_image": shot["output"]["image_path"],
                "output_path": shot["output"]["video_path"],
            })
    return path


def export_edl(data):
    path = OUT_DIR / "edit_decision_list.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    edl = [
        {
            "id": shot["id"],
            "title": shot["title"],
            "timestamp": shot["timestamp"],
            "duration_seconds": shot["duration_seconds"],
            "video_path": shot["output"]["video_path"],
            "narration_beat": shot["narration_beat"],
        }
        for shot in data["shots"]
    ]
    path.write_text(json.dumps(edl, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main():
    data = load_shots()
    outputs = [
        export_image_prompts(data),
        export_video_prompts(data),
        export_edl(data),
    ]
    print("Atlas ONE builder complete.")
    for p in outputs:
        print(p)


if __name__ == "__main__":
    main()

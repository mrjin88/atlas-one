#!/usr/bin/env python3
"""
Atlas ONE File-Driven Builder

Run from an LA-xxxx project folder:

    python E:\atlas-one\system\builders\build_batches.py

Outputs:
    exports/archive/image_prompt_batch.csv
    exports/archive/video_prompt_batch.csv
    exports/archive/edit_decision_list.csv
"""

from pathlib import Path
import csv
import yaml

root = Path.cwd()
shots_path = root / "shots.yaml"
out = root / "exports" / "archive"
out.mkdir(parents=True, exist_ok=True)

data = yaml.safe_load(shots_path.read_text(encoding="utf-8"))
shots = data["shots"]

with (out / "image_prompt_batch.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "title", "prompt", "negative_prompt", "output_path"])
    w.writeheader()
    for s in shots:
        w.writerow({
            "id": s["id"],
            "title": s["title"],
            "prompt": s["image_prompt"],
            "negative_prompt": s["negative_prompt"],
            "output_path": s["output"]["image_path"],
        })

with (out / "video_prompt_batch.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "title", "prompt", "reference_image", "output_path"])
    w.writeheader()
    for s in shots:
        w.writerow({
            "id": s["id"],
            "title": s["title"],
            "prompt": s["video_prompt"],
            "reference_image": s["output"]["image_path"],
            "output_path": s["output"]["video_path"],
        })

with (out / "edit_decision_list.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "timestamp", "duration_seconds", "video_path", "narration_beat"])
    w.writeheader()
    for s in shots:
        w.writerow({
            "id": s["id"],
            "timestamp": s["timestamp"],
            "duration_seconds": s["duration_seconds"],
            "video_path": s["output"]["video_path"],
            "narration_beat": s["narration_beat"],
        })

print("Build complete.")
print(out)

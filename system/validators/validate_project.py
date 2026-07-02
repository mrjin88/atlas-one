#!/usr/bin/env python3
r"""
Atlas ONE File-Driven Validator

Run from any LA-xxxx project folder:

    python E:\atlas-one\system\validators\validate_project.py
"""

from pathlib import Path
import sys
import yaml

REQUIRED_FILES = [
    "research.md",
    "script.md",
    "timeline.md",
    "shots.md",
    "shots.yaml",
    "review.md",
    "publish_checklist.md",
    "seo.json",
]

REQUIRED_DIRS = [
    "assets/images",
    "assets/videos",
    "assets/voice",
    "assets/music",
    "assets/sfx",
    "assets/thumbnail",
    "exports/youtube",
    "exports/shorts",
    "exports/archive",
]

VALID_EVIDENCE = {"HIGH", "MEDIUM", "LOW", "SPECULATION"}

def fail(msg):
    print(f"[FAIL] {msg}")
    return 1

def ok(msg):
    print(f"[OK] {msg}")

def main():
    root = Path.cwd()
    errors = 0

    for f in REQUIRED_FILES:
        if not (root / f).exists():
            errors += fail(f"Missing file: {f}")
        else:
            ok(f"File exists: {f}")

    for d in REQUIRED_DIRS:
        if not (root / d).exists():
            errors += fail(f"Missing folder: {d}")
        else:
            ok(f"Folder exists: {d}")

    shots_file = root / "shots.yaml"
    if shots_file.exists():
        data = yaml.safe_load(shots_file.read_text(encoding="utf-8"))
        shots = data.get("shots", []) if isinstance(data, dict) else []
        ids = [s.get("id") for s in shots]

        if len(ids) != len(set(ids)):
            errors += fail("Duplicate shot IDs found")
        else:
            ok("Shot IDs are unique")

        for shot in shots:
            sid = shot.get("id", "UNKNOWN")
            if shot.get("evidence_level") not in VALID_EVIDENCE:
                errors += fail(f"{sid}: invalid evidence_level")
            if not shot.get("image_prompt"):
                errors += fail(f"{sid}: missing image_prompt")
            if not shot.get("video_prompt"):
                errors += fail(f"{sid}: missing video_prompt")
            if not shot.get("negative_prompt"):
                errors += fail(f"{sid}: missing negative_prompt")
            if int(shot.get("duration_seconds", 0)) > 12:
                errors += fail(f"{sid}: duration too long")

    if errors:
        print(f"\nValidation failed with {errors} error(s).")
        sys.exit(1)

    print("\nValidation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()

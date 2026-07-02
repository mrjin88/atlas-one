#!/usr/bin/env python3
"""
Atlas ONE - create_project.py

Usage:
    python create_project.py --root E:\atlas-one\projects\lost-archive\content --id LA-0002 --slug forgotten-steel
"""

from pathlib import Path
import argparse
import json

FILES = [
    "research.md",
    "script.md",
    "timeline.md",
    "shots.md",
    "shots.yaml",
    "review.md",
    "publish_checklist.md",
]

FOLDERS = [
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

def touch(path: Path, content=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--id",required=True)
    ap.add_argument("--slug",required=True)
    args=ap.parse_args()

    project=Path(args.root)/f"{args.id}-{args.slug}"

    project.mkdir(parents=True,exist_ok=True)

    for f in FOLDERS:
        (project/f).mkdir(parents=True,exist_ok=True)

    for f in FILES:
        touch(project/f, f"# {f}\n")

    seo={
        "project_id":args.id,
        "slug":args.slug,
        "title":"",
        "description":"",
        "tags":[],
        "chapters":[]
    }
    touch(project/"seo.json", json.dumps(seo,indent=2))

    print(f"Created: {project}")

if __name__=="__main__":
    main()

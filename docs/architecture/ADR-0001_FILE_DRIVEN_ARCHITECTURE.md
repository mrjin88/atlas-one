# ADR-0001 --- Atlas ONE Repository Architecture

Status: ACCEPTED

## Decision

Atlas ONE adopts a **file-driven architecture**.

Human-maintained source files:

-   research.md
-   script.md
-   shots.yaml
-   review.md
-   publish_checklist.md
-   seo.json

Generated artifacts:

generated/ - timeline.md - shots.md - image_prompt_batch.csv -
video_prompt_batch.csv - edit_decision_list.csv

## Rules

1.  `shots.yaml` is the only editable production database.
2.  Never edit files inside `generated/`.
3.  Builders always regenerate `generated/`.
4.  Validators must validate `shots.yaml` before any build.
5.  Research and script remain human-readable Markdown.

## Project Layout

``` text
LA-xxxx/
├── research.md
├── script.md
├── shots.yaml
├── review.md
├── publish_checklist.md
├── seo.json
├── assets/
├── exports/
└── generated/
```

## Build Pipeline

research.md ↓ script.md ↓ shots.yaml ↓ validate ↓ build ↓ generated/ ↓
render ↓ publish

## Next Engineering Tasks

-   build_timeline.py
-   build_shots_md.py
-   build_batches.py
-   validate_project.py
-   atlas CLI

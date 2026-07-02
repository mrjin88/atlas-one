# Atlas ONE Core Architecture v1

## Mission

Atlas ONE is a video production operating system.

The source of truth is a **Project Object**, not a collection of
markdown files.

------------------------------------------------------------------------

# Core

    atlas/
    ├── core/
    ├── builder/
    ├── exporter/
    ├── validator/
    ├── cli/
    └── templates/

------------------------------------------------------------------------

# Responsibilities

## core/

Owns the project model.

    Project
     ├── metadata
     ├── research
     ├── script
     ├── timeline
     ├── shots
     ├── assets
     ├── seo
     └── publish

No renderer, exporter or AI provider is allowed to modify this object
directly.

------------------------------------------------------------------------

## builder/

Transforms Project → production artifacts.

Outputs:

-   research.md
-   script.md
-   timeline.md
-   shots.md
-   shots.yaml

------------------------------------------------------------------------

## exporter/

Converts Project into external formats.

Targets:

-   Veo
-   Kling
-   Flux
-   Midjourney
-   ElevenLabs
-   DaVinci Resolve
-   Premiere
-   YouTube upload metadata

------------------------------------------------------------------------

## validator/

Checks project integrity.

Rules include:

-   required fields
-   duplicate shot IDs
-   missing prompts
-   invalid durations
-   invalid evidence levels
-   missing assets

Validation must fail before rendering if errors exist.

------------------------------------------------------------------------

## cli/

Public commands.

    atlas create
    atlas validate
    atlas build
    atlas export
    atlas render
    atlas publish

------------------------------------------------------------------------

# Canonical Project Lifecycle

    Topic
       ↓
    Project Object
       ↓
    Research
       ↓
    Script
       ↓
    Timeline
       ↓
    Shots
       ↓
    Validation
       ↓
    Build
       ↓
    Export
       ↓
    Generate Assets
       ↓
    Edit
       ↓
    Publish

------------------------------------------------------------------------

# Repository Layout

    atlas-one/
    │
    ├── atlas/
    │   ├── core/
    │   ├── builder/
    │   ├── exporter/
    │   ├── validator/
    │   ├── cli/
    │   └── templates/
    │
    ├── projects/
    │
    └── docs/

------------------------------------------------------------------------

# Design Principles

1.  One Source of Truth.
2.  Deterministic builds.
3.  Immutable shot IDs.
4.  Providers are replaceable.
5.  Project data is separate from generated assets.
6.  Markdown is an export format, not the canonical model.
7.  Every builder is stateless.

------------------------------------------------------------------------

# Immediate Refactor Plan

1.  Replace `system/` with `atlas/`.
2.  Introduce `Project` model.
3.  Make `shots.yaml` the canonical shot database.
4.  Generate markdown from the Project model.
5.  Replace standalone scripts with CLI commands.

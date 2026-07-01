# CE-001 Code Review — Content Engine Refactor (ADR-001 Compliance)

## Git Status

```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        atlas-core/
        docs/DEVELOPMENT_ENVIRONMENT.md

nothing added to commit but untracked files present (use "git add" to track)
```

## Git Diff — Stat

No tracked files were modified. All changes are in the new `atlas-core/content-engine/` directory (untracked).

## Files in Scope

```
atlas-core/content-engine/
├── __init__.py
├── engine.py
├── models.py
├── pipeline.py
├── README.md
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── image_prompt.py
│   ├── publish.py
│   ├── research.py
│   ├── script.py
│   ├── seo.py
│   └── video_prompt.py
└── tests/
    └── test_pipeline.py
```

## Architecture Changes

### Before (AIP-0005)

- `ContentEngine` contained all generation logic directly (research, script, prompts, SEO, publishing)
- No provider abstraction or interface
- Monolithic design — violated ADR-001

### After (CE-001)

- **Provider interface** (`providers/base.py`) — abstract base class with `generate(idea)` contract
- **6 concrete providers** — `ResearchProvider`, `ScriptProvider`, `ImagePromptProvider`, `VideoPromptProvider`, `SEOProvider`, `PublishProvider`
- **ContentEngine** — now an orchestrator that dispatches to providers by key, owns no generation logic
- **ContentPipeline** — remains responsible for execution order and result assembly
- `models.py` — unchanged (still `ContentPlan` dataclass)
- All imports use direct module references (no relative imports for portability)

### Key Files — Content

**providers/base.py** — Abstract provider contract:
```python
class Provider(ABC):
    @abstractmethod
    def generate(self, idea: str) -> Any:
        raise NotImplementedError
```

**engine.py** — Orchestrator (no generation logic):
```python
class ContentEngine:
    def __init__(self, providers=None):
        self._providers = providers or self._default_providers()

    def run(self, idea: str) -> Dict[str, List[str]]:
        results: Dict[str, List[str]] = {}
        for key, provider_cls in self._providers.items():
            provider = provider_cls()
            results[key] = provider.generate(idea)
        return results
```

**pipeline.py** — Pipeline now consumes dict from engine:
```python
class ContentPipeline:
    def run(self, idea: str) -> PipelineResult:
        results = self.engine.run(idea)
        return PipelineResult(
            idea=idea,
            research=results.get("research", []),
            script=results.get("script", []),
            image_prompts=results.get("image_prompts", []),
            video_prompts=results.get("video_prompts", []),
            seo=results.get("seo", []),
            publish_checklist=results.get("publish_checklist", []),
        )
```

## Test Results

```
E:\atlas-one> python -m pytest atlas-core/content-engine/tests -q
.                                                                        [100%]
1 passed in 0.04s
```

All assertions pass, including verification of exact output strings from each provider.

## Summary

- ADR-001 compliance achieved
- Clean separation of concerns between orchestrator (engine), execution order (pipeline), and implementation (providers)
- Provider interface makes future providers pluggable without modifying the engine
- All placeholder generation moved out of engine into dedicated provider classes
- Tests updated and passing

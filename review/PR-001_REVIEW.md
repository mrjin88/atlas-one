# Pull Request Review — PR #1

## Pull Request Summary

| Field | Value |
|---|---|
| **Branch** | `feature/ce-002-provider-registry` |
| **Base** | `main` |
| **Commit** | `cd25772` |
| **Message** | `feat(content-engine): add provider registry` |
| **Status** | Open |

Implements `ProviderRegistry` as the single source of truth for content pipeline providers and refactors `ContentEngine` to consume providers through the registry instead of importing concrete provider classes directly.

## Files Changed

| File | Status | Δ (lines) |
|---|---|---|
| `atlas-core/content-engine/providers/registry.py` | **Added** | +44 |
| `atlas-core/content-engine/tests/test_registry.py` | **Added** | +68 |
| `atlas-core/content-engine/engine.py` | Modified | −9 net |
| `atlas-core/content-engine/pipeline.py` | Modified | +15 net |
| `atlas-core/content-engine/providers/__init__.py` | Modified | +2 |

Plus binary pycache updates (4 files).

## Architecture Impact

**Before:** `ContentEngine` imported all six concrete providers and maintained a hardcoded dictionary mapping names to provider classes. Adding a new provider required modifying the engine.

**After:** `ContentEngine` accepts an optional `ProviderRegistry`. It discovers providers by querying the registry's `list()` and `get()` methods. The engine has zero knowledge of concrete provider classes — it works with any `Provider` subtype registered in the registry.

**Registration boundary:** The default provider wiring moved from `engine.py` to `pipeline.py` (the `_default_registry()` factory), which is the natural entry point for application-level composition.

## Public API Changes

| Symbol | Change |
|---|---|
| `ProviderRegistry` | **New** — class with `register()`, `get()`, `list()`, `exists()`, `unregister()` |
| `ContentEngine.__init__` | Parameter changed from `providers: Dict[str, Type[Provider]] | None` to `registry: ProviderRegistry | None` |
| `ContentPipeline.__init__` | No signature change; internally creates engine with a registry-backed default |

## Breaking Changes

- `ContentEngine.__init__(providers=...)` is **removed**. Any code constructing `ContentEngine` with the `providers` dict parameter will break. The new parameter is `registry`.
- No other public API breaks.

## Test Results

```
E:\atlas-one> python -m pytest atlas-core/content-engine/tests -q
..........                                                               [100%]
10 passed in 0.07s
```

- 1 existing pipeline test — unchanged, still passes
- 9 new registry tests — all green

## Git Diff (--stat)

```
 .../__pycache__/engine.cpython-314.pyc             | Bin 2678 -> 1824 bytes
 .../__pycache__/pipeline.cpython-314.pyc           | Bin 2710 -> 3948 bytes
 atlas-core/content-engine/engine.py                |  36 +++--------
 atlas-core/content-engine/pipeline.py              |  23 ++++++-
 atlas-core/content-engine/providers/__init__.py    |   2 +
 .../providers/__pycache__/__init__.cpython-314.pyc | Bin 619 -> 674 bytes
 .../providers/__pycache__/registry.cpython-314.pyc | Bin 0 -> 3425 bytes
 atlas-core/content-engine/providers/registry.py    |  44 +++++++++++++
 .../test_registry.cpython-314-pytest-9.1.1.pyc     | Bin 0 -> 12484 bytes
 atlas-core/content-engine/tests/test_registry.py   |  68 +++++++++++++++++++++
 10 files changed, 146 insertions(+), 27 deletions(-)
```

## Full Git Diff

### engine.py (core change)

```diff
-from typing import Dict, List, Type
-from providers import Provider
-from providers.research import ResearchProvider
-from providers.script import ScriptProvider
-from providers.image_prompt import ImagePromptProvider
-from providers.video_prompt import VideoPromptProvider
-from providers.seo import SEOProvider
-from providers.publish import PublishProvider
+from typing import Dict, List
+from providers.registry import ProviderRegistry

 class ContentEngine:
     def __init__(
         self,
-        providers: Dict[str, Type[Provider]] | None = None,
+        registry: ProviderRegistry | None = None,
     ) -> None:
-        self._providers = providers or self._default_providers()
+        self._registry = registry or ProviderRegistry()

     def run(self, idea: str) -> Dict[str, List[str]]:
         results: Dict[str, List[str]] = {}
-        for key, provider_cls in self._providers.items():
+        for name in self._registry.list():
+            provider_cls = self._registry.get(name)
             provider = provider_cls()
-            results[key] = provider.generate(idea)
+            results[name] = provider.generate(idea)
         return results
```

### registry.py (new file)

```python
class ProviderRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Type[Provider]] = {}

    def register(self, name: str, provider: Type[Provider]) -> None:
        if name in self._registry:
            raise ValueError(f"Provider '{name}' is already registered.")
        self._registry[name] = provider

    def get(self, name: str) -> Type[Provider]:
        if name not in self._registry:
            raise KeyError(f"Provider '{name}' is not registered.")
        return self._registry[name]

    def list(self) -> List[str]:
        return sorted(self._registry.keys())

    def exists(self, name: str) -> bool:
        return name in self._registry

    def unregister(self, name: str) -> None:
        if name not in self._registry:
            raise KeyError(f"Provider '{name}' is not registered.")
        del self._registry[name]
```

## Self Review

### What was improved

- **Clean Architecture compliance:** `ContentEngine` is now a pure orchestrator with no dependency on concrete provider classes
- **Extensibility:** New providers can be added by registering them in the registry — no engine modification required
- **Testability:** The registry can be populated with mock providers for isolated engine tests
- **Single source of truth:** Provider registration is centralized rather than scattered across code paths
- **Clear error handling:** Duplicate registration raises `ValueError`; missing provider lookup raises `KeyError`

### Risks

- Breaking change to `ContentEngine` constructor signature — any external code using the old `providers` parameter will need updating
- `__pycache__` files continue to be tracked in git (pre-existing issue, not introduced by this change)

### Future improvements

- Add a `deregister_all()` or `reset()` method for test teardown convenience
- Consider a `load()` / `discover()` method that scans a namespace for provider implementations
- Add `pycache` entries to `.gitignore` to keep the diff clean
- Consider making `_default_registry()` a public API so consumers can customize the registry before passing it to the engine

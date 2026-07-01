from __future__ import annotations

from typing import Dict, List, Type

from providers import Provider
from providers.research import ResearchProvider
from providers.script import ScriptProvider
from providers.image_prompt import ImagePromptProvider
from providers.video_prompt import VideoPromptProvider
from providers.seo import SEOProvider
from providers.publish import PublishProvider


class ContentEngine:
    """Orchestrator that coordinates independent providers.

    The engine does not own generation logic. It dispatches work to
    providers and collects their outputs.
    """

    def __init__(
        self,
        providers: Dict[str, Type[Provider]] | None = None,
    ) -> None:
        self._providers = providers or self._default_providers()

    @staticmethod
    def _default_providers() -> Dict[str, Type[Provider]]:
        return {
            "research": ResearchProvider,
            "script": ScriptProvider,
            "image_prompts": ImagePromptProvider,
            "video_prompts": VideoPromptProvider,
            "seo": SEOProvider,
            "publish_checklist": PublishProvider,
        }

    def run(self, idea: str) -> Dict[str, List[str]]:
        results: Dict[str, List[str]] = {}
        for key, provider_cls in self._providers.items():
            provider = provider_cls()
            results[key] = provider.generate(idea)
        return results

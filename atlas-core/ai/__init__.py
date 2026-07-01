"""AI provider abstraction layer for Atlas ONE."""

try:
    from .base import AIProvider
    from .registry import AIProviderRegistry
    from .mock import MockProvider
    from .providers.openai_provider import (
        MissingAPIKeyError,
        OpenAIProvider,
        OpenAIProviderError,
    )
except ImportError:
    from base import AIProvider
    from registry import AIProviderRegistry
    from mock import MockProvider
    from providers.openai_provider import (  # type:ignore[no-redef]
        MissingAPIKeyError,
        OpenAIProvider,
        OpenAIProviderError,
    )


__all__ = [
    "AIProvider",
    "AIProviderRegistry",
    "MockProvider",
    "OpenAIProvider",
    "MissingAPIKeyError",
    "OpenAIProviderError",
]


__all__ = ["AIProvider", "AIProviderRegistry", "MockProvider"]

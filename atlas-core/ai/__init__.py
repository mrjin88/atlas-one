"""AI provider abstraction layer for Atlas ONE."""

try:
    from .base import AIProvider
    from .registry import AIProviderRegistry
    from .mock import MockProvider
    from .providers.openai_provider import (
        MissingAPIKeyError,
        OpenAIAPIError,
        OpenAIProvider,
    )
except ImportError:
    from base import AIProvider
    from registry import AIProviderRegistry
    from mock import MockProvider
    from providers.openai_provider import (  # type:ignore[no-redef]
        MissingAPIKeyError,
        OpenAIAPIError,
        OpenAIProvider,
    )


__all__ = [
    "AIProvider",
    "AIProviderRegistry",
    "MockProvider",
    "OpenAIProvider",
    "MissingAPIKeyError",
    "OpenAIAPIError",
]


__all__ = ["AIProvider", "AIProviderRegistry", "MockProvider"]

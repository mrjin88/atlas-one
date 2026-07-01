# ADR-001: Content Engine Orchestration

- **Title:** Content Engine as Orchestrator
- **Status:** Accepted

## Context

The initial implementation of the content engine placed business logic directly inside the engine layer. This approach made the component responsible for multiple distinct concerns, including research preparation, script generation, prompt creation, SEO planning, and publishing preparation.

As Atlas ONE grows, this creates a maintenance problem. The engine becomes harder to extend, harder to test in isolation, and less compatible with future provider-specific implementations. A clearer architectural model is needed.

## Decision

Atlas Core will follow an orchestration architecture.

The Content Engine will act as an orchestrator rather than a monolithic implementation layer. Its responsibility is to coordinate execution across independent providers. It will not directly own the logic for research generation, script generation, prompt generation, SEO generation, or publishing generation.

In this model:

- ContentPipeline orchestrates execution
- Providers implement specific capabilities
- The engine coordinates inputs, outputs, and workflow sequencing

Example provider roles include:

- ResearchProvider
- ScriptProvider
- PromptProvider
- SEOProvider
- PublishProvider

Future providers may include:

- PodcastProvider
- LinkedInProvider
- InstagramProvider
- TikTokProvider
- NewsletterProvider

## Consequences

### Advantages

- Clear separation of responsibilities
- Easier extension for new content formats and channels
- Better testability of individual provider behavior
- Improved reuse of provider logic across projects
- Stronger alignment with Atlas ONE's modular architecture

### Disadvantages

- Requires additional abstraction and interface design
- Introduces more moving parts than a simple monolithic engine
- Requires disciplined coordination between orchestrator and providers

### Trade-offs

The system becomes more modular and maintainable, but it also requires more structural discipline. This trade-off is appropriate for a platform intended to evolve over time.

## Alternatives Considered

### Monolithic Engine

A single engine could continue to own all generation logic. This would simplify the initial implementation but would make the system harder to evolve and harder to reuse across providers.

### Hybrid Approach

A hybrid model could mix orchestrator logic with some provider-specific behavior inside the engine. This would reduce initial structure but would weaken the boundaries that Atlas ONE needs for long-term growth.

## Examples

A typical content workflow would proceed as follows:

1. ContentPipeline receives an idea
2. The pipeline invokes a ResearchProvider
3. The pipeline invokes a ScriptProvider
4. The pipeline invokes a PromptProvider
5. The pipeline invokes an SEOProvider
6. The pipeline invokes a PublishProvider
7. The pipeline returns a structured output package

This structure allows each provider to evolve independently while the pipeline remains responsible for sequencing and integration.

## Future Impact

This decision establishes the architectural direction for future engine development. It provides a foundation for additional providers, additional content formats, and richer multi-channel publishing workflows. It also ensures that Atlas Core remains extensible rather than becoming a tightly coupled implementation layer.

# Engineering Principles

## Purpose

These principles define how engineering work is performed at Atlas ONE. They are the operating rules for human developers, AI developers, reviewers, and future contributors. The goal is to ensure that work remains consistent, reviewable, reusable, and aligned with the platform's long-term architecture.

## Core Engineering Principles

### Systems over Hacks

Atlas ONE should favor durable systems over short-term shortcuts. Temporary solutions may be acceptable in the short term, but they should not become the default pattern. Engineering work should improve the platform's structure, maintainability, and clarity.

### Documentation First

Every significant change should be documented in a way that makes intent understandable. Documentation is part of the implementation, not an afterthought. This includes architectural decisions, process changes, task context, and user-facing documentation where needed.

### AI Executes, Humans Decide

AI systems may generate implementations, draft assets, and accelerate execution, but humans remain responsible for judgment, approval, and final direction. The role of AI is to support execution, not replace accountability.

### Human Review Required

No change should be treated as complete until it has been reviewed. Review ensures correctness, consistency, and alignment with platform standards. This applies to code, prompts, templates, workflows, and documentation.

### One AIP = One Asset = One Commit

Each implementation task should produce a clear, reviewable unit of work. A single change request should map to a single meaningful asset or deliverable and be committed as a focused unit. This reduces ambiguity and improves traceability.

### Version Everything

Prompts, templates, workflows, assets, documents, and code should be versioned where appropriate. Versioning provides traceability, supports recovery, and makes it easier to understand what changed and why.

### Build Once Publish Everywhere

Engineering decisions should be made with reuse in mind. A capability should be built once and adapted for multiple outputs or channels rather than duplicated across projects.

### Small Iterations

Work should be delivered in small, reviewable increments. Large changes should be broken into manageable steps that can be understood, tested, and improved over time.

### Reuse Before Rebuild

Before creating new infrastructure, the team should look for existing assets that can be reused or extended. Rebuilding should be avoided unless it clearly improves the system.

### Simplicity Over Cleverness

The preferred solution is the one that is easiest to understand, maintain, and review. Cleverness is acceptable only when it significantly improves clarity or maintainability.

## Engineering Workflow

```text
Vision
↓
Architecture
↓
Engineering Principles
↓
AIP
↓
Implementation
↓
Review
↓
Approval
↓
Commit
↓
Release
```

Every task should follow this progression. Work should not skip directly from idea to implementation without architectural context or review.

## AI Collaboration

Atlas ONE depends on a clear division of responsibility between human and AI contributors.

### CEO

The CEO represents product intent, direction, and strategic priorities. The CEO defines what matters and what should be prioritized.

### CTO

The CTO maintains technical direction and ensures that work remains aligned with the platform architecture. The CTO evaluates system fit and architectural soundness.

### AI Developer

The AI developer is responsible for generating implementation work, drafting assets, producing documentation, and supporting execution within the agreed scope. The AI developer must operate within the principles of review, clarity, and reuse.

### Reviewer

The reviewer evaluates whether the work meets requirements, aligns with standards, and is safe to merge. Review should focus on correctness, completeness, and maintainability.

### Future Contributors

Future contributors should be able to understand the intent of the work, the decisions behind it, and the expected standards for delivery. Every contribution should be understandable to the next engineer or AI developer.

## Definition of Done

A task is not complete until all of the following are true:

- Requirements completed
- Documentation updated
- Review passed
- No unfinished TODOs
- Ready for production

Completion should not be inferred from partial implementation or an unfinished draft.

## Engineering Rules

The following rules are mandatory:

- Never implement before architecture
- Never bypass review
- Never duplicate functionality when reuse is possible
- Never commit unreviewed work
- Always document decisions
- Always prefer reusable assets
- Always keep the system understandable
- Always preserve traceability for important changes

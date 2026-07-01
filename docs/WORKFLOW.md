# Atlas ONE Development Workflow

## Purpose

This workflow defines how Atlas ONE is developed, reviewed, approved, and released. It exists to make execution consistent across human contributors, AI contributors, and future teams. The workflow connects strategy, architecture, implementation, review, and delivery into a repeatable operating process.

## Development Lifecycle

```text
Business Idea
↓
Vision
↓
Architecture
↓
Engineering Principles
↓
AIP
↓
AI Implementation
↓
CTO Review
↓
CEO Approval
↓
Commit
↓
Push
↓
Release
```

Each stage should be completed in order unless a documented exception is approved. The workflow is designed to keep the project aligned with its purpose while preserving review and accountability.

## Sprint Workflow

```text
Sprint Planning
↓
AIP Creation
↓
Implementation
↓
Review
↓
Revision (if needed)
↓
Approval
↓
Commit
↓
Push
↓
Close Sprint
```

Sprint planning identifies the work that matters most for the next delivery cycle. Each sprint should produce a small number of clearly defined implementation units that can be reviewed and approved efficiently.

## AI Collaboration Workflow

```text
CEO
↓
CTO
↓
AI Developer
↓
Reviewer
```

### CEO

The CEO provides direction, business intent, and prioritization. The CEO ensures that work remains aligned with the long-term mission of Atlas ONE.

### CTO

The CTO ensures that the work is technically coherent, compatible with the architecture, and suitable for long-term platform growth.

### AI Developer

The AI developer implements the requested work within the agreed scope. The AI developer is responsible for generating clear deliverables, documenting changes, and preparing work for review.

### Reviewer

The reviewer verifies correctness, clarity, completeness, and maintainability. Review is mandatory before approval and commit.

## Review Workflow

```text
Draft
↓
Technical Review
↓
Revision
↓
Approval
↓
Commit
```

A draft should be reviewed for technical correctness, alignment with existing standards, and completeness. Revisions should be made before approval. Once approved, the work is ready to be committed.

## Git Workflow

```text
One AIP
↓
One Asset
↓
One Commit
↓
One Push
```

Each task should be scoped to a single AIP and a single meaningful asset or deliverable. The implementation should be committed as one focused change and pushed once it is approved.

## Document Lifecycle

```text
Draft
↓
Review
↓
Approved
↓
Versioned
↓
Archived (if replaced)
```

Documents should evolve through review and approval rather than remain as unstructured drafts. Once approved, they should be versioned and preserved as part of the project record. If replaced, older versions should be archived clearly.

## Workflow Rules

The following rules apply to all work at Atlas ONE:

- Never skip review
- Never commit draft work
- Never modify multiple assets in one AIP
- Always preserve history
- Always document important decisions
- Always keep implementation aligned with the current architecture and principles
- Always prefer clarity and maintainability over speed alone

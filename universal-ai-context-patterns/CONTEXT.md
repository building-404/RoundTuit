# ICM — Routing

Entry point for task routing. Read this first, then follow the pointer.

---

## Quick Navigation

| Task | Go to |
|------|-------|
| New .NET API project | `prompts/new-dotnet-api.md` |
| Update existing .NET API | `prompts/update-dotnet-api.md` |
| Content pipeline | `prompts/content-pipeline.md` |
| Business process modernization | `prompts/business-process-modernization.md` |
| Clean code review | `prompts/clean-code-review.md` |
| Current task status | `.universal-mwp/context/active-context.md` |
| Pending approvals | `.universal-mwp/queue/approvals.md` |
| Learned preferences | `MEMORY_HOME/icm/preferences.db` (universal) + `.universal-mwp/preferences.local.yaml` (overrides) |
| Project conventions | `references/conventions.md` |
| Rate limiting | `references/rate-limiting.md` |
| Refactoring patterns | `references/refactoring.md` |

---

## Session Start

1. Read `IDENTITY.md` for workspace structure
2. Read `.universal-mwp/protocol/tick-contract.md` for execution rules
3. Check `.universal-mwp/context/active-context.md` for current task
4. Read `.universal-mwp/queue/inbox.md` for pending tasks
5. Execute tick per tick-contract.md

---

## Reusable .NET API Stages

Workflow prompts define which stages run. The numbered stages below are shared instructions for .NET API workflows, not a single sequence required by every workflow. Stage 5 is used by the new API workflow; it is not a standalone workflow.

| # | Stage | File |
|---|-------|------|
| 1 | Research | `pipelines/01-research.md` |
| 2 | Structuring | `pipelines/02-structuring.md` |
| 3 | Code Generation | `pipelines/03-code-generation.md` |
| 4 | Documentation | `pipelines/04-documentation.md` |
| 5 | Proof of Concept | `pipelines/05-proof-of-concept.md` |

Each stage file contains: inputs, process, outputs, human check, and next pointer.

---

## Risk Classification

| Change Scope | Risk | Action |
|--------------|------|--------|
| read-only | low | Auto-execute |
| new-file | low | Auto-execute |
| modify-existing | medium | Request approval |
| delete | high | Require confirmation |
| external-integration | high | Require confirmation |

Full rules: `.universal-mwp/policy/local-tick.yaml`

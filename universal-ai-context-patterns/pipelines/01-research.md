# Stage 1: Research

Understand requirements and existing codebase structure.

---

## Purpose

Catalog the current state and identify gaps between requirements and implementation.

---

## Inputs

| File | Description |
|------|-------------|
| `.universal-mwp/REQUIREMENTS.md` | What to build |
| `.universal-mwp/context/tech-context.md` | Stack, dependencies |
| Template/existing code path | Source material |

---

## Process

1. Load requirements from source (issue tracker, inline, or file)
2. Catalog existing structure (messages, handlers, decorators)
3. Identify gaps between requirements and current state
4. Execute research phases:
   - **Inventory**: Project structure, patterns, registrations
   - **Thematic Extraction**: CQRS patterns, decorator chains, OpResult usage
   - **Gap Analysis**: What's needed vs what exists
   - **Synthesis**: Implementation plan
   - **Brief**: Key decisions and assumptions
5. Save research outputs

---

## Outputs

| Path | Description |
|------|-------------|
| `{{CONTEXT_PATH}}/research/` | Research artifacts |
| `{{CONTEXT_PATH}}/research/STAGE_COMPLETE.md` | Completion gate |

---

## Human Check

Before proceeding, verify:
- [ ] All requirements are accounted for
- [ ] Gap analysis is accurate
- [ ] Implementation plan is realistic

---

## Next

Stage 2: Structuring → `pipelines/02-structuring.md`

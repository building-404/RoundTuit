# Stage 2: Structuring

Map requirements to architecture and plan implementation.

---

## Purpose

Define the structure of the solution before generating code.

---

## Inputs

| File | Description |
|------|-------------|
| `.universal-mwp/STANDARDS.json` | Code style guidelines |
| `.universal-mwp/context/product-context.md` | Domain constraints |
| `{{CONTEXT_PATH}}/research/` | Stage 1 outputs |

---

## Process

1. Map each requirement to: Message class + Handler + DataAccess + Tests
2. Define decorator chain for new features
3. Plan CompositionRoot registrations
4. Structure documentation outline (README, API docs, ADRs)
5. Save structure plan

---

## Outputs

| Path | Description |
|------|-------------|
| `{{CONTEXT_PATH}}/script-lab/` | Structure artifacts |
| `{{CONTEXT_PATH}}/script-lab/STAGE_COMPLETE.md` | Completion gate |

---

## Human Check

Before proceeding, verify:
- [ ] All features are mapped to handlers
- [ ] Decorator chain is correct
- [ ] No circular dependencies

---

## Next

Stage 3: Code Generation → `pipelines/03-code-generation.md`

# Stage 3: Code Generation

Generate or modify code following established patterns.

---

## Purpose

Produce working code from the structure plan.

---

## Inputs

| File | Description |
|------|-------------|
| `.universal-mwp/STANDARDS.json` | Code style guidelines |
| `.universal-mwp/context/tech-context.md` | Stack, dependencies |
| `{{CONTEXT_PATH}}/script-lab/` | Stage 2 outputs |

---

## Process

1. Scaffold solution (replace "Template" with `{{PROJECT_NAME}}`)
2. Generate per feature:
   - Message classes (Command/Query)
   - Handlers
   - DataAccess interfaces and implementations
   - Tests
3. Apply SOLID principles
4. Wire CompositionRoot (decorator order preserved)
5. Update Permissions.cs with new permissions
6. Audit against conventions

---

## Outputs

| Path | Description |
|------|-------------|
| `.universal-mwp/OUTPUT/src/` | Generated code |
| `{{CONTEXT_PATH}}/code-gen/STAGE_COMPLETE.md` | Completion gate |

---

## Human Check

Before proceeding, verify:
- [ ] Code compiles
- [ ] Tests pass
- [ ] Decorator order is correct
- [ ] No missing permissions

---

## Next

Stage 4: Documentation → `pipelines/04-documentation.md` (if applicable)

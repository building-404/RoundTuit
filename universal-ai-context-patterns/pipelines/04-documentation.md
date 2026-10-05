# Stage 4: Documentation

Generate comprehensive documentation for the project.

---

## Purpose

Create documentation that explains the solution and guides future developers.

---

## Inputs

| File | Description |
|------|-------------|
| `{{CONTEXT_PATH}}/script-lab/` | Stage 2 outputs |
| `.universal-mwp/OUTPUT/src/` | Generated code |

---

## Process

1. Generate project README.md:
   - Setup instructions
   - Configuration options
   - Deployment guide
2. Generate API documentation:
   - Endpoint catalog (commands/queries, routes, permissions)
   - Authentication & authorization model
   - Error handling patterns (OpResult responses)
3. Generate architecture decision records (ADRs):
   - Why CQRS + decorator chain
   - Data access strategy
   - Deviations from template defaults

---

## Outputs

| Path | Description |
|------|-------------|
| `.universal-mwp/OUTPUT/docs/README.md` | Project README |
| `.universal-mwp/OUTPUT/docs/api-endpoints.md` | API catalog |
| `.universal-mwp/OUTPUT/docs/architecture-decisions.md` | ADRs |
| `{{CONTEXT_PATH}}/STAGE_COMPLETE.md` | Completion gate (docs) |

---

## Human Check

Before proceeding, verify:
- [ ] README is accurate and complete
- [ ] All endpoints are documented
- [ ] ADRs explain key decisions

---

## Next

The new .NET API workflow continues to Stage 5: Proof of Concept → `pipelines/05-proof-of-concept.md`. Other workflows invoke only the stages defined by their workflow prompt.

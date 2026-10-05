# Stage 5: Proof of Concept

Validate riskiest assumptions with minimal code.

---

## Purpose

Prove that the hardest parts of the implementation will work before committing to full implementation.

---

## Inputs

| File | Description |
|------|-------------|
| `.universal-mwp/REQUIREMENTS.md` | What to build |
| `.universal-mwp/OUTPUT/src/` | Generated code |

---

## Process

1. Identify the highest-risk or least-understood requirement
2. Generate a minimal PoC that validates:
   - Data access pattern works for chosen database
   - Decorator chain handles custom cross-cutting concern
   - Third-party integration connects successfully
3. Include a PoC-specific test that proves the concept
4. Document what the PoC validates and what remains unproven

---

## Outputs

| Path | Description |
|------|-------------|
| `.universal-mwp/OUTPUT/poc/` | PoC code + tests |
| `.universal-mwp/OUTPUT/poc/poc-validation.md` | Validation report |
| `{{CONTEXT_PATH}}/STAGE_COMPLETE.md` | Completion gate (poc) |

---

## Human Check

Before marking complete, verify:
- [ ] PoC runs successfully
- [ ] Test proves the concept
- [ ] Validation report is accurate

---

## Next

Pipeline complete. Return to `CONTEXT.md` for next task.

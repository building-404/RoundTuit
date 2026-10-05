# ICM Protocol — Signal Logging & Rule Derivation

Canonical mechanics for how the system learns preferences. All ICM skills
(`/approve`, `/auto-approve`, `/complete`, and any decision point) reference
THIS file so the behavior is defined in one place (DRY).

State lives in:
- `icm/preference-signals.json` — raw observed signals (schema `local-icm/preference-signals@1`)
- `icm/preference-rules.yaml` — derived + seed rules (with confidence)
- `icm/decision-log.md` — human-readable audit trail of decisions

---

## 1. When to log a signal

Log a signal whenever the user does any of the following about a task or action:
- **approves** or gives an inline go-ahead ("work X", "start it", "implement")
- **rejects** or reverts something
- **corrects** how a task was done (tooling, format, scope)
- sets a **standing instruction** ("always do X", "never do Y")
- confirms a **guardrail** (stops an action)

Read-only ticks with no user decision do not produce signals.

---

## 2. Signal format (append to `preference-signals.json` → `signals[]`)

```json
{
  "id": "sig-NNN",
  "date": "YYYY-MM-DD",
  "task": "{task id or short label}",
  "observation": "{what happened, ideally quoting the user}",
  "signal_type": "approval_granted | rejection | correction | correction_persistent | guardrail | implicit_accept",
  "dimensions": { "task_type": "...", "risk_assigned": "...", "...": "..." }
}
```

- `id` is the next `sig-NNN` in sequence.
- Keep `dimensions` free-form but consistent — they are what rules match on.

---

## 3. Rule derivation

After appending a signal, check whether it should update `preference-rules.yaml`:

1. **Standing instruction / persistent correction / guardrail** → derive or
   update a rule immediately, even from a single signal. Set a conservative
   confidence (0.8–0.95) and list the signal id in `based_on`.
2. **Repeated pattern** → when **3+** signals share the same
   `signal_type` + key `dimensions`, derive a rule. Confidence scales with
   count/consistency (e.g. 3 → ~0.8, 5+ consistent → ~0.9).
3. **Conflicting signals** → lower the confidence of the affected rule, or
   split into more specific conditions. Never silently overwrite; note the
   conflict in `decision-log.md`.

Rule shape (see `preference-rules.yaml`):

```yaml
- id: rule-{slug}
  when: { situation: "..." }        # or task_type/target/side_effects keys
  prefer: "{what to do next time}"
  confidence: 0.0-1.0
  based_on: ["sig-NNN", ...]
  notes: "optional"
```

Rules with `confidence >= 0.8` may be applied automatically; lower-confidence
rules are advisory and must still surface to the user. All rules are
human-editable.

---

## 4. Applying rules (Read/Classify phase)

At the start of a tick, load `preference-rules.yaml`. Before classifying or
stopping for approval, check for a matching rule:
- A matching `confidence >= 0.8` rule adjusts behavior automatically
  (e.g. `rule-inline-goahead-is-approval` skips the stop-and-wait cycle;
  `rule-complete-when-done` auto-completes finished work).
- Record any auto-application in `decision-log.md`.

---

## 5. Decision log entry (append to `decision-log.md`)

```
## {date} — {task}
- Decision: {what was decided}
- Basis: {signal id(s) / rule id(s), or "new signal"}
- Risk: {low|medium|high} (change_scope: {scope})
```

---

## Notes
- This protocol is the single source of truth for ICM mechanics. The
  `tick-contract.md` Learn phase and the approve/auto-approve/complete skills
  all defer here rather than restating the format.
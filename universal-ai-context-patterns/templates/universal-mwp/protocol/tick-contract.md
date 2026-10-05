# Tick Contract

Canonical execution rules for the Universal AI Context Patterns system.

## Execution Model

Each chat invocation is one **deterministic tick**. State persists across sessions via local files.

### Tick Flow

1. **Read Phase**: Load context, queue, ICM rules/signals
2. **Classify Phase**: Determine change_scope → risk (per policy/local-tick.yaml)
3. **Execute Phase**:
   - Low risk: execute immediately
   - Medium/High risk: request approval, stop (unless a confidence >= 0.8 rule
     such as rule-inline-goahead-is-approval applies)
4. **Write Phase**: Update state files
5. **Learn Phase**: Log signals → derive rules in ICM (see protocol/icm-protocol.md)

## Risk Classification

Classified by `change_scope` in `policy/local-tick.yaml` (first match wins):

| Change scope | Risk | Action |
|--------------|------|--------|
| read-only | low | Auto-execute |
| new-file | low | Auto-execute |
| modify-existing | medium | Request approval |
| delete | high | Require confirmation |
| external-integration | high | Require confirmation |

## ICM Learning Protocol

Signal logging and rule derivation mechanics are defined canonically in
`protocol/icm-protocol.md` (single source of truth). In brief:

```
Signal → Rule Derivation → Auto-Adjustment

1. On any user decision (approve / reject / correct / standing instruction),
   append a signal to icm/preference-signals.json (schema preference-signals@1).
2. Derive/update a rule in icm/preference-rules.yaml:
   - persistent correction / guardrail / standing instruction → rule from 1 signal
   - repeated pattern → rule after 3+ consistent signals
   Confidence scales with count/consistency; >= 0.8 may auto-apply.
3. Next matching tick → apply the rule; record it in icm/decision-log.md.
```

## Tick Output

After each tick, output a brief summary:
- Task executed/approved/blocked
- Files modified
- ICM signals logged

## State Files

| File | Purpose |
|------|---------|
| `context/active-context.md` | Current task being worked |
| `context/progress.md` | Completed work log |
| `context/tech-context.md` | Durable technical facts |
| `context/product-context.md` | Product/domain intent |
| `queue/inbox.md` | Pending tasks |
| `queue/approvals.md` | Pending approvals |
| `icm/preference-signals.json` | Raw decision signals (preference-signals@1) |
| `icm/preference-rules.yaml` | Derived + seed rules |
| `icm/decision-log.md` | Human-readable decision audit trail |
| `policy/local-tick.yaml` | Scope-based risk classification |
| `conventions/*.md` | Durable project standards (e.g. pr-review) |
| `reviews/` | Archived reviews (YYYYMMDD-HHMMSS-slug.md) |
| `archived/YYYYMMDD/` | Archived task artifacts |
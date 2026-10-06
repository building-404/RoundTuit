# Tick Contract

Canonical execution rules for the Universal AI Context Patterns system.

## Execution Model

Each chat invocation is one **deterministic tick**. State persists across sessions via local files.

### Tick Flow

1. **Read Phase**: Load context, queue, and preference rules
   - Load per-project context: `context/active-context.md`, `context/progress.md`
   - Load task queue: `queue/inbox.md`, `queue/approvals.md`
   - Load preference rules from universal memory:
     `~/.ai-context/memory/icm/preferences.db` (universal rules table)
   - Load project-specific overrides if present:
     `<workspace>/.universal-mwp/preferences.local.yaml`
   - Resolution order: local overrides → project-pattern rules → universal rules → defaults
2. **Classify Phase**: Determine change_scope → risk (per policy/local-tick.yaml)
3. **Execute Phase**:
   - Low risk: execute immediately
   - Medium/High risk: request approval, stop (unless a confidence >= 0.8 rule
     such as rule-inline-goahead-is-approval applies)
4. **Write Phase**: Update state files
5. **Learn Phase**: Log signals → derive rules in universal memory
   - Write signal to `~/.ai-context/memory/icm/preferences.db` signals table
   - Run rule derivation (see protocol/icm-protocol.md §3)
   - Write decision to decisions table
   - Do NOT write to per-project `icm/preference-signals.json` (deprecated)
   Full mechanics: `protocol/icm-protocol.md`

### Memory Bootstrap

On every tick start, before the Read Phase, verify universal memory exists:

1. Check if `~/.ai-context/memory/icm/preferences.db` exists
2. If not, create the directory structure and initialize the database:
   - Create `~/.ai-context/memory/icm/` and `~/.ai-context/memory/icm/archive/`
   - Initialize `preferences.db` with the schema defined in `references/universal-memory-spec.md`
   - Log: "Universal memory initialized at ~/.ai-context/memory/"
3. If yes, check if a daily archive is due:
   - Query: `SELECT value FROM meta WHERE key = 'last_archive_at'`
   - If null or more than 24 hours ago, run the archive process (see icm-protocol.md §6)
   - Check for rules with `pending_review = 1` and surface them (see below)

### Pending Rule Reviews

If any rules have `pending_review = 1` after archive runs, surface them before
proceeding with the current tick:

```
{N} rule(s) pending review after archive:
  - {rule_id} (confidence: {confidence}, last applied: {last_applied_at})
    Keep active? [yes / no / make permanent]
```

- `yes` — clears `pending_review`, rule remains as-is
- `no` — sets `is_active = 0`
- `make permanent` — sets `is_permanent = 1`, rule is never flagged for review again

Record the review decision in the universal decisions table.

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
   INSERT a signal into ~/.ai-context/memory/icm/preferences.db (signals table).
2. Derive/update a rule in the universal rules table:
   - persistent correction / guardrail / standing instruction → rule from 1 signal
   - repeated pattern → rule after 3+ consistent signals
   Confidence scales with count/consistency; >= 0.8 may auto-apply.
3. Next matching tick → apply the rule; record it in the decisions table.
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
| `policy/local-tick.yaml` | Scope-based risk classification |
| `conventions/*.md` | Durable project standards (e.g. pr-review) |
| `reviews/` | Archived reviews (YYYYMMDD-HHMMSS-slug.md) |
| `archived/YYYYMMDD/` | Archived task artifacts |
| `preferences.local.yaml` | Project-specific preference overrides (optional) |
| `~/.ai-context/memory/icm/preferences.db` | Universal signals, rules, decisions (SQLite, hot 28-day window) |
| `~/.ai-context/memory/icm/archive/YYYY-MM.parquet` | Archived signals and decisions (cold, monthly) |
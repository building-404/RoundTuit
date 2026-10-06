# Universal Memory — Implementation Changes

**Status**: Draft  
**Version**: 0.1  
**Date**: 2026-10-06  
**Associated spec**: `universal-memory-spec.md`

This document contains the exact instruction text changes required to implement
universal memory. These changes are applied to `tick-contract.md` and
`icm-protocol.md` when the owner approves implementation. Do not apply until the
spec and this document are approved.

---

## Changes to `tick-contract.md`

### 1. Add Memory Bootstrap Check (new section, after Tick Flow)

Add the following section after the `### Tick Flow` section:

```markdown
### Memory Bootstrap

On every tick start, before the Read Phase, verify universal memory exists:

1. Check if `~/.ai-context/memory/icm/preferences.db` exists
2. If not, create the directory structure and initialize the database:
   - Create `~/.ai-context/memory/icm/` and `~/.ai-context/memory/icm/archive/`
   - Initialize `preferences.db` with the schema defined in `universal-memory-spec.md`
   - Log: "Universal memory initialized at ~/.ai-context/memory/"
3. If yes, check if a daily archive is due:
   - Query: `SELECT MAX(last_archive_at) FROM meta`
   - If null or more than 24 hours ago, run the archive process (see ICM Protocol §6)
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
```

---

### 2. Update Read Phase

Replace the current Read Phase step:

**Current**:
```markdown
1. **Read Phase**: Load context, queue, ICM rules/signals
```

**Replace with**:
```markdown
1. **Read Phase**: Load context, queue, and preference rules
   - Load per-project context: `context/active-context.md`, `context/progress.md`
   - Load task queue: `queue/inbox.md`, `queue/approvals.md`
   - Load preference rules from universal memory:
     `~/.ai-context/memory/icm/preferences.db` (universal rules table)
   - Load project-specific overrides if present:
     `<workspace>/.universal-mwp/preferences.local.yaml`
   - Resolution order: local overrides → project-pattern rules → universal rules → defaults
```

---

### 3. Update Learn Phase

Replace the current Learn Phase step:

**Current**:
```markdown
5. **Learn Phase**: Log signals → derive rules in ICM (see protocol/icm-protocol.md)
```

**Replace with**:
```markdown
5. **Learn Phase**: Log signals → derive rules in universal memory
   - Write signal to `~/.ai-context/memory/icm/preferences.db` signals table
   - Run rule derivation (see protocol/icm-protocol.md §3)
   - Write decision to decisions table
   - Do NOT write to per-project `icm/preference-signals.json` (deprecated)
   Full mechanics: `protocol/icm-protocol.md`
```

---

### 4. Update State Files Table

Add/update the following rows in the State Files table:

**Remove** (deprecated):
```
| `icm/preference-signals.json` | Raw decision signals (preference-signals@1) |
| `icm/preference-rules.yaml`   | Derived + seed rules |
| `icm/decision-log.md`         | Human-readable decision audit trail |
```

**Add** (universal memory):
```
| `~/.ai-context/memory/icm/preferences.db` | Universal signals, rules, decisions (SQLite, hot 28-day window) |
| `~/.ai-context/memory/icm/archive/YYYY-MM.parquet` | Archived signals and decisions (cold, monthly) |
| `<workspace>/.universal-mwp/preferences.local.yaml` | Project-specific preference overrides (optional) |
```

---

## Changes to `icm-protocol.md`

### 1. Update State Files Header

**Current**:
```markdown
State lives in:
- `icm/preference-signals.json` — raw observed signals (schema `local-icm/preference-signals@1`)
- `icm/preference-rules.yaml` — derived + seed rules (with confidence)
- `icm/decision-log.md` — human-readable audit trail of decisions
```

**Replace with**:
```markdown
State lives in universal memory at `~/.ai-context/memory/icm/preferences.db`:
- `signals` table — raw observed signals (rolling 28-day hot window)
- `rules` table — derived + seed rules (with confidence, permanent until reviewed)
- `decisions` table — audit trail of rule applications and manual decisions

Cold archive (>28 days) lives in `~/.ai-context/memory/icm/archive/YYYY-MM.parquet`.

Project-specific overrides (optional, take precedence over universal rules):
- `<workspace>/.universal-mwp/preferences.local.yaml`
```

---

### 2. Update §2 Signal Format

**Current**:
```markdown
## 2. Signal format (append to `preference-signals.json` → `signals[]`)
```

**Replace with**:
```markdown
## 2. Signal format (INSERT into `preferences.db` → `signals` table)

```sql
INSERT INTO signals (
  project_path, project_name, task_id, task_type, risk_level,
  action, confidence, context_json
) VALUES (
  '<absolute-workspace-path>',
  '<project-name>',
  '<task-id-or-short-label>',
  '<task_type>',        -- feature, bugfix, chore, correction, guardrail, etc.
  '<risk_level>',       -- low, medium, high
  '<action>',           -- approved, denied, deferred, corrected, guardrail
  <confidence>,         -- 1.0 for explicit decisions, lower for implicit
  '<json-context>'      -- see context_json shape below
);
```

**Field semantics**:

- `task_type` — what kind of work it was: `feature`, `bugfix`, `chore`, `correction`, `guardrail`
- `risk_level` — the classified risk at time of decision: `low`, `medium`, `high`
- `action` — what the user did: `approved`, `denied`, `deferred`, `corrected`, `guardrail`
- `confidence` — signal strength: `1.0` for explicit decisions (approve/deny), lower for implicit accepts
- `context_json` — free-form JSON capturing observation and match dimensions:

```json
{
  "observation": "user approved medium-risk feature without hesitation",
  "signal_type": "approval_granted",
  "dimensions": {
    "task_type": "feature",
    "risk_assigned": "medium",
    "had_tests": true
  }
}
```

`signal_type` values: `approval_granted` | `rejection` | `correction` | `correction_persistent` | `guardrail` | `implicit_accept`

Keep `dimensions` keys consistent across signals — they are what rules pattern-match on. A rule derived from signals with `dimensions.task_type = "feature"` only matches future signals with that same dimension key.
```

---

### 3. Update §3 Rule Derivation

**Current**:
```markdown
After appending a signal, check whether it should update `preference-rules.yaml`:
```

**Replace with**:
```markdown
After inserting a signal, check whether it should update the `rules` table:
```

Replace the rule shape YAML example with:

```markdown
```sql
INSERT OR REPLACE INTO rules (
  rule_id, project_pattern, condition_json, action,
  confidence, signal_count, is_permanent
) VALUES (
  'rule-{slug}',
  NULL,                   -- NULL = universal; or glob pattern for project-specific
  '{"task_type": "...", "risk_level": "..."}',
  'auto_approve',         -- auto_approve | require_approval | auto_deny
  0.85,
  3,
  0
);
```

Rules with `confidence >= 0.8` may be applied automatically. Rules with
`is_permanent = 1` are never flagged for review at archive time. All rules
remain human-editable via direct SQLite query or `preferences.local.yaml`
override.
```

---

### 4. Update §4 Applying Rules

**Current**:
```markdown
At the start of a tick, load `preference-rules.yaml`.
```

**Replace with**:
```markdown
At the start of a tick, query applicable rules from universal memory:

```sql
SELECT * FROM rules
WHERE is_active = 1
  AND (project_pattern IS NULL
       OR project_pattern = '<project_path>'
       OR '<project_path>' GLOB project_pattern)
  AND json_extract(condition_json, '$.task_type') = '<task_type>'
  AND json_extract(condition_json, '$.risk_level') = '<risk_level>'
ORDER BY
  CASE WHEN project_pattern IS NOT NULL THEN 0 ELSE 1 END,
  confidence DESC
LIMIT 1;
```

Then check `<workspace>/.universal-mwp/preferences.local.yaml` for overrides.
Local overrides take precedence over all database rules.
```

---

### 5. Update §5 Decision Log

**Current**:
```markdown
## 5. Decision log entry (append to `decision-log.md`)
```

**Replace with**:
```markdown
## 5. Decision log entry (INSERT into `preferences.db` → `decisions` table)

```sql
INSERT INTO decisions (
  project_path, task_id, rule_id, decision, reasoning
) VALUES (
  '<absolute-workspace-path>',
  '<task-id>',
  '<rule-id-or-NULL>',   -- NULL if manual decision with no matching rule
  '<decision>',          -- approved, denied, deferred
  '<reasoning>'          -- brief explanation
);
```
```

---

### 6. Add §6 Archive Process (new section)

Add the following as a new section at the end of `icm-protocol.md`:

```markdown
## 6. Archive Process

Run on first tick of each day if `meta.last_archive_at` is older than 24 hours.

### Step 1 — Export to Parquet

For each month group of records older than 28 days:

```sql
SELECT 'signals' as tbl, project_path, project_name, task_id, task_type,
       risk_level, action, confidence, context_json, created_at
FROM signals WHERE created_at < date('now', '-28 days')
UNION ALL
SELECT 'decisions', project_path, task_id, rule_id, decision,
       reasoning, NULL, NULL, NULL, created_at
FROM decisions WHERE created_at < date('now', '-28 days');
```

Append results to `~/.ai-context/memory/icm/archive/YYYY-MM.parquet`
(one file per month, append-mode).

### Step 2 — Delete from SQLite

```sql
DELETE FROM signals WHERE created_at < date('now', '-28 days');
DELETE FROM decisions WHERE created_at < date('now', '-28 days');
```

### Step 3 — Flag rules for review

```sql
UPDATE rules
SET pending_review = 1
WHERE is_permanent = 0
  AND is_active = 1
  AND signal_count > 0
  AND rule_id NOT IN (
    SELECT DISTINCT json_extract(context_json, '$.rule_id')
    FROM signals
    WHERE json_extract(context_json, '$.rule_id') IS NOT NULL
  );
```

### Step 4 — Update archive timestamp

```sql
INSERT OR REPLACE INTO meta (key, value)
VALUES ('last_archive_at', datetime('now'));
```

### DuckDB Cross-Archive Queries (Optional)

To query across hot (SQLite) and cold (Parquet) data, use DuckDB:

```sql
SELECT task_type, risk_level, COUNT(*) as total,
  SUM(CASE WHEN action = 'approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as approval_rate
FROM (
  SELECT task_type, risk_level, action FROM signals
  UNION ALL
  SELECT task_type, risk_level, action
  FROM read_parquet('~/.ai-context/memory/icm/archive/*.parquet')
  WHERE tbl = 'signals'
)
GROUP BY task_type, risk_level;
```

DuckDB is not required for daily operation. Install: `brew install duckdb`.
```

---

## Changes to `install/INSTALL.md`

### Add to Step 1 — Install the shared engine

After the existing Step 1 content, add:

```markdown
### Step 1b — Initialize universal memory (always)

1. Ensure `~/.ai-context/memory/icm/` exists (create parents as needed)
2. Ensure `~/.ai-context/memory/icm/archive/` exists
3. If `~/.ai-context/memory/icm/preferences.db` does not exist, initialize it:
   - Create `signals`, `rules`, `decisions`, and `meta` tables per the schema
     in `references/universal-memory-spec.md`
4. If `~/.ai-context/memory/templates/` does not exist, copy
   `ENGINE_HOME/templates/preferences.local.yaml` to
   `~/.ai-context/memory/templates/preferences.local.yaml`

This initializes the universal memory store. It is safe to re-run — existing
data is not overwritten.
```

---

## Schema: `meta` Table (addition to spec)

The archive process requires a `meta` table not in the current spec. Add to `preferences.db`:

```sql
CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

-- Seed on init
INSERT OR IGNORE INTO meta (key, value) VALUES ('last_archive_at', NULL);
INSERT OR IGNORE INTO meta (key, value) VALUES ('schema_version', '1');
```

---

## Migration Note

When this implementation is applied:

1. Per-project `icm/` folders become deprecated but are not immediately deleted
2. On first tick after update, existing `icm/preference-signals.json` signals
   are migrated to the universal DB automatically:

```markdown
Migration step (first tick only, per project):
- If `<workspace>/.universal-mwp/icm/preference-signals.json` exists:
  - Read all signals
  - INSERT each into universal `signals` table with `project_path` set
  - Rename file to `icm/preference-signals.json.migrated`
- If `<workspace>/.universal-mwp/icm/preference-rules.yaml` exists:
  - Read all rules
  - INSERT each into universal `rules` table with `project_pattern` set to project path
  - Rename file to `icm/preference-rules.yaml.migrated`
- Log migration result in universal `decisions` table
```

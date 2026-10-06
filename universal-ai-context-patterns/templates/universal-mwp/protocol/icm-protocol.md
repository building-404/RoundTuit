# ICM Protocol — Signal Logging & Rule Derivation

Canonical mechanics for how the system learns preferences. All ICM skills
(`/approve`, `/auto-approve`, `/complete`, and any decision point) reference
THIS file so the behavior is defined in one place (DRY).

State lives in universal memory at `~/.ai-context/memory/icm/preferences.db`:
- `signals` table — raw observed signals (rolling 28-day hot window)
- `rules` table — derived + seed rules (with confidence, permanent until reviewed)
- `decisions` table — audit trail of rule applications and manual decisions

Cold archive (>28 days) lives in `~/.ai-context/memory/icm/archive/YYYY-MM.parquet`.

Project-specific overrides (optional, take precedence over universal rules):
- `<workspace>/.universal-mwp/preferences.local.yaml`

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

---

## 3. Rule derivation

After inserting a signal, check whether it should update the `rules` table:

1. **Standing instruction / persistent correction / guardrail** → derive or
   update a rule immediately, even from a single signal. Set a conservative
   confidence (0.8–0.95) and list the signal id in `based_on`.
2. **Repeated pattern** → when **3+** signals share the same
   `signal_type` + key `dimensions`, derive a rule. Confidence scales with
   count/consistency (e.g. 3 → ~0.8, 5+ consistent → ~0.9).
3. **Conflicting signals** → lower the confidence of the affected rule, or
   split into more specific conditions. Never silently overwrite; record the
   conflict in the decisions table.

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

---

## 4. Applying rules (Read/Classify phase)

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

A matching `confidence >= 0.8` rule adjusts behavior automatically
(e.g. `rule-inline-goahead-is-approval` skips the stop-and-wait cycle;
`rule-complete-when-done` auto-completes finished work).
Record any auto-application in the decisions table.

---

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

---

## 6. Archive Process

Run on first tick of each day if `meta.last_archive_at` is older than 24 hours.

### Step 1 — Export to Parquet

For each month group of records older than 28 days, append to
`~/.ai-context/memory/icm/archive/YYYY-MM.parquet`:

```sql
SELECT 'signals' as tbl, project_path, project_name, task_id, task_type,
       risk_level, action, confidence, context_json, created_at
FROM signals WHERE created_at < date('now', '-28 days')
UNION ALL
SELECT 'decisions', project_path, task_id, rule_id, decision,
       reasoning, NULL, NULL, NULL, created_at
FROM decisions WHERE created_at < date('now', '-28 days');
```

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

To query across hot (SQLite) and cold (Parquet) data, use DuckDB
(`brew install duckdb`):

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

DuckDB is not required for daily operation. SQLite handles all runtime queries.

---

## Notes
- This protocol is the single source of truth for ICM mechanics. The
  `tick-contract.md` Learn phase and the approve/auto-approve/complete skills
  all defer here rather than restating the format.
- Per-project `icm/` folders (`preference-signals.json`, `preference-rules.yaml`,
  `decision-log.md`) are deprecated. Existing data is migrated to universal memory
  on first tick after this update.
# Universal Memory Scripts

Agent-runnable instructions for the universal memory maintenance scripts.
All scripts live in `universal-ai-context-patterns/scripts/` and operate on
`~/.ai-context/memory/icm/preferences.db`.

**Dependencies**: Python 3.10+, `pyarrow` (archive only), `pyyaml` (migrate only)

```bash
pip install pyarrow pyyaml
```

---

## archive.py — Daily archive (SQLite → Parquet)

Flushes signals and decisions older than 28 days to monthly Parquet files
and flags rules for review whose source signals have all been archived.

**When to run**: Automatically on first tick of each day (per icm-protocol.md §6).
The script skips if archive ran < 24 hours ago.

```bash
# Normal run (skips if not due)
python universal-ai-context-patterns/scripts/archive.py

# Force run regardless of last archive time
python universal-ai-context-patterns/scripts/archive.py --force
```

**Output**:
```
  Archived 47 records → 2026-09.parquet
  Archived 12 records → 2026-08.parquet

Archive complete:
  52 signals archived
  7 decisions archived
  2 rule(s) flagged for review

  Run 'python review_rules.py' to review pending rules.
```

---

## review_rules.py — Review rules pending after archive

Surfaces rules flagged for review and prompts for keep / disable / make permanent.

**When to run**: After archive flags rules, or any time you want to audit active rules.

```bash
# Interactive review
python universal-ai-context-patterns/scripts/review_rules.py

# List pending rules without prompting
python universal-ai-context-patterns/scripts/review_rules.py --list
```

**Interactive prompt**:
```
[1] auto-approve-feature-medium
    scope:        universal
    condition:    {"task_type": "feature", "risk_level": "medium"}
    action:       auto_approve
    confidence:   0.85
    signal count: 5
    last applied: 2026-09-28T14:22:00

    Keep active? [yes / no / permanent / skip]:
```

- `yes` — clears pending_review, rule stays active as-is
- `no` — disables the rule (is_active = 0)
- `permanent` — keeps active and marks is_permanent = 1 (never flagged again)
- `skip` — leaves pending_review = 1, prompts again next session

---

## migrate.py — One-time migration from per-project ICM to universal memory

Reads per-project `icm/preference-signals.json` and `icm/preference-rules.yaml`
and migrates them to `~/.ai-context/memory/icm/preferences.db`.

**When to run**: Once, after universal memory is initialized. Safe to re-run —
already-migrated records are skipped.

```bash
# Preview what would be migrated (no writes)
python universal-ai-context-patterns/scripts/migrate.py --dry-run

# Migrate all projects found under HOME
python universal-ai-context-patterns/scripts/migrate.py

# Migrate a single project
python universal-ai-context-patterns/scripts/migrate.py --project /path/to/project
```

**Output**:
```
Found 3 project(s) to migrate.

  my-api
    signals: 23
    rules:   4
  content-project
    signals: 8
    rules:   2
  old-project
    signals: 0
    rules:   1

Migration complete:
  31 signals migrated
  7 rules migrated

  Source files renamed to *.migrated (not deleted).
  Remove them manually once you've verified the migration.
```

After migration, source files are renamed to `*.migrated` — not deleted.
Verify the DB contents before removing them.

---

## Agent Instructions

When icm-protocol.md §6 triggers archive, run:

```
python universal-ai-context-patterns/scripts/archive.py
```

If the output includes "rule(s) flagged for review", surface the count to the
user and offer to run the review script in the same session or defer to next session.

For first-time setup after install, prompt the user:

```
Found per-project ICM data. Migrate to universal memory?
Run: python universal-ai-context-patterns/scripts/migrate.py --dry-run
```

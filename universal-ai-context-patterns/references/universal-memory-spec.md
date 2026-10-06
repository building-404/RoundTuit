# Universal Memory Architecture Specification

**Status**: Draft  
**Version**: 0.1  
**Date**: 2026-10-05

---

## Overview

This specification defines a universal memory layer for the MWP (Model Workspace Protocol) system, enabling cross-project preference learning while reducing per-project repository footprint.

### Storage Model

| Layer | Format | Retention | Purpose |
|-------|--------|-----------|---------|
| Hot | SQLite | Rolling 28 days | Day-to-day rule resolution, signal recording |
| Cold | Parquet | Indefinite | Historical analytics, pattern discovery |
| Overrides | YAML | Manual | Project-specific human-editable preferences |
| Analytics | DuckDB | N/A | Optional unified query layer across hot + cold |

**Archive trigger**: Daily on first use. Any signals or decisions older than 28 days are flushed to the appropriate monthly Parquet file before the tick runs.

**Rule retention**: Rules are permanent until archive runs. At archive time, any rule whose supporting signals have all moved to archive is flagged for review in the next session. The rule remains active while pending — it does not stop auto-applying until the human explicitly changes or disables it.

---

## Existing Convention: `~/.ai-context/`

The `~/.ai-context/` directory is an established convention in this project for global, user-level AI context storage. It is defined in `install/INSTALL.md` as:

> **ENGINE_HOME** — the shared engine home (plain path):  
> `HOME/.ai-context/universal-ai-context-patterns`

### Current Structure

```
~/.ai-context/
└── universal-ai-context-patterns/     # The shared engine
    ├── IDENTITY.md                    # Layer 0 — workspace map
    ├── CONTEXT.md                     # Layer 1 — task routing
    ├── pipelines/                     # Layer 2 — numbered stage files
    ├── prompts/                       # Executable workflow prompts
    ├── conventions/                   # Coding + workflow standards
    ├── references/                    # Stable reference material
    ├── templates/                     # Per-project state templates
    │   └── universal-mwp/             # Skeleton for new projects
    └── .kiro/skills/                  # Kiro slash-command skills
```

### Design Principles

From `install/INSTALL.md`:

1. **Global engine, gitignored project state** — The engine installs once to a shared global home
2. **No project-committed files** — Everything is global/user-level via each tool's global config
3. **Single source of truth** — One engine shared across Kiro, Claude, Gemini, Copilot, Amazon Q
4. **Per-project state is gitignored** — `.universal-mwp/` is created on first use and excluded from source control

---

## Proposed Extension: Universal Memory

Universal memory extends the existing `~/.ai-context/` convention by adding a new sibling to the engine:

```
~/.ai-context/
├── universal-ai-context-patterns/     # Engine (existing, read-only)
│   ├── IDENTITY.md
│   ├── CONTEXT.md
│   ├── pipelines/
│   ├── prompts/
│   ├── conventions/
│   ├── references/
│   └── templates/
│
└── memory/                            # Universal memory (NEW, read-write)
    ├── icm/
    │   ├── preferences.db             # SQLite: hot window (rolling 28 days)
    │   ├── preferences.db-wal         # SQLite WAL files
    │   ├── preferences.db-shm
    │   └── archive/                   # Parquet: monthly cold archives
    │       ├── 2026-10.parquet
    │       ├── 2026-09.parquet
    │       └── ...
    └── templates/
        └── preferences.local.yaml     # Template for project overrides
```

### Why This Location

| Factor | Rationale |
|--------|-----------|
| **Consistency** | Follows the established `~/.ai-context/` convention |
| **Separation** | Memory is sibling to engine, not inside it (engine remains read-only) |
| **Tool-agnostic** | Same location works for all wired AI tools |
| **Gitignored by default** | User-level directory, never committed to any project |
| **Portable** | Single directory to backup/restore all learned preferences |

---

## Current vs Proposed Architecture

### Current: Per-Project Memory

```
~/.ai-context/
└── universal-ai-context-patterns/     # Engine only

project-a/
└── .universal-mwp/
    ├── icm/
    │   ├── preference-signals.json    # 50 signals (project A only)
    │   ├── preference-rules.yaml      # 5 rules
    │   └── decision-log.md
    ├── context/
    ├── queue/
    └── protocol/

project-b/
└── .universal-mwp/
    ├── icm/
    │   ├── preference-signals.json    # 30 signals (project B only, relearning)
    │   ├── preference-rules.yaml      # 4 rules
    │   └── decision-log.md
    ├── context/
    ├── queue/
    └── protocol/
```

**Problems**:
- Learning doesn't transfer between projects
- Per-project memory footprint (`icm/` folder)
- Relearning similar patterns for each project
- No cross-project pattern analysis

### Proposed: Universal Memory

```
~/.ai-context/
├── universal-ai-context-patterns/     # Engine (unchanged)
│
└── memory/                            # NEW: Universal memory
    ├── icm/
    │   └── preferences.db             # All signals + rules across ALL projects
    └── templates/
        └── preferences.local.yaml

project-a/
└── .universal-mwp/
    ├── context/                       # Current task state (kept)
    ├── queue/                         # Tasks and approvals (kept)
    ├── protocol/                      # Execution rules (kept)
    └── preferences.local.yaml         # Project-specific overrides (optional)

project-b/
└── .universal-mwp/
    ├── context/
    ├── queue/
    ├── protocol/
    └── preferences.local.yaml         # Project-specific overrides (optional)
```

**Benefits**:
- Learning transfers across projects
- Smaller per-project footprint (no `icm/` folder)
- Single source of truth for preferences
- Cross-project pattern analysis enabled
- Project-specific overrides available when needed

---

## Database Schema

### Location

```
~/.ai-context/memory/icm/preferences.db
```

### Tables

```sql
-- Preference signals: raw observations of user decisions
CREATE TABLE signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_path TEXT NOT NULL,           -- Absolute path to project
  project_name TEXT,                    -- Human-readable name
  task_id TEXT NOT NULL,
  task_type TEXT NOT NULL,              -- feature, bugfix, chore, etc.
  risk_level TEXT NOT NULL,             -- low, medium, high
  action TEXT NOT NULL,                 -- approved, denied, deferred
  confidence REAL DEFAULT 1.0,          -- Signal strength (0.0-1.0)
  context_json TEXT,                    -- Additional context as JSON
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  
  UNIQUE(project_path, task_id)         -- Prevent duplicate signals
);

-- Derived rules: patterns extracted from signals
CREATE TABLE rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_id TEXT NOT NULL UNIQUE,         -- Human-readable ID
  project_pattern TEXT,                 -- NULL = universal, else glob pattern
  condition_json TEXT NOT NULL,         -- Match conditions as JSON
  action TEXT NOT NULL,                 -- auto_approve, require_approval, auto_deny
  confidence REAL NOT NULL,             -- 0.0-1.0
  signal_count INTEGER NOT NULL,        -- Supporting signal count
  derived_at TEXT NOT NULL DEFAULT (datetime('now')),
  last_applied_at TEXT,
  is_active BOOLEAN NOT NULL DEFAULT 1,
  human_override TEXT,
  pending_review BOOLEAN NOT NULL DEFAULT 0,  -- Flagged when source signals archived
  is_permanent BOOLEAN NOT NULL DEFAULT 0,    -- Never flagged for review again
  
  CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

-- Decision log: record of rule applications
CREATE TABLE decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_path TEXT NOT NULL,
  task_id TEXT NOT NULL,
  rule_id TEXT,                         -- NULL if manual decision
  decision TEXT NOT NULL,
  reasoning TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  
  FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
);

-- Indexes for common queries
CREATE INDEX idx_signals_project ON signals(project_path);
CREATE INDEX idx_signals_type_risk ON signals(task_type, risk_level);
CREATE INDEX idx_rules_project_pattern ON rules(project_pattern);
CREATE INDEX idx_rules_active ON rules(is_active);
CREATE INDEX idx_decisions_project_task ON decisions(project_path, task_id);
```

---

## Archive Process

### Trigger

On first use each day, before any tick runs:

1. Query signals and decisions older than 28 days
2. Group by month (`strftime('%Y-%m', created_at)`)
3. For each month group, append to `~/.ai-context/memory/icm/archive/YYYY-MM.parquet`
4. Delete archived rows from SQLite
5. Check rules whose all supporting signals are now archived — flag for review

### Rule Review Flagging

After archive runs, any rule where all source signals have moved to archive is marked `pending_review` in the rules table:

```sql
UPDATE rules
SET pending_review = 1
WHERE signal_count > 0
  AND id NOT IN (
    SELECT DISTINCT derived_from_signal_id FROM signals
  );
```

On the next session start, the agent surfaces pending rules:

```
1 rule pending review:
  - auto-approve feature+medium (confidence: 0.85, last applied: 2026-09-28)
  Keep active? [yes / no / make permanent]
```

`make permanent` removes the review requirement — the rule never gets flagged again regardless of archive cycles.

### Archive Schema (Parquet)

Each monthly Parquet file contains the same columns as the SQLite `signals` and `decisions` tables, plus a `table` column to distinguish them:

```
archive/2026-10.parquet
  columns: table, id, project_path, project_name, task_id, task_type,
           risk_level, action, confidence, context_json, created_at
```

---

## DuckDB: Unified Query Layer (Optional)

DuckDB is a recommended optional dependency for analytics queries across hot (SQLite) and cold (Parquet) data. It requires no server — single binary, works on macOS/Linux/Windows.

### Cross-Archive Query Example

```sql
-- Approval rate across all time (hot + cold)
SELECT task_type, risk_level,
  SUM(CASE WHEN action = 'approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS approval_rate,
  COUNT(*) AS total
FROM (
  SELECT task_type, risk_level, action FROM signals  -- hot (SQLite)
  UNION ALL
  SELECT task_type, risk_level, action              -- cold (Parquet)
  FROM read_parquet('~/.ai-context/memory/icm/archive/*.parquet')
  WHERE table = 'signals'
)
GROUP BY task_type, risk_level
ORDER BY total DESC;
```

### Installation

```bash
# macOS
brew install duckdb

# Direct download
curl -L https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-osx-universal.zip -o duckdb.zip
```

DuckDB is **not required** for daily operation. SQLite handles all runtime queries. DuckDB is only needed when querying historical archives.

---

When classifying a new task, rules are resolved in priority order:

```
1. Project-specific overrides (preferences.local.yaml)
2. Rules matching project pattern (rules.project_pattern matches current project)
3. Universal rules (rules.project_pattern IS NULL)
4. Built-in defaults
```

### Query Pattern

```sql
SELECT * FROM rules
WHERE is_active = 1
  AND (project_pattern IS NULL 
       OR project_pattern = ?
       OR ? GLOB project_pattern)
  AND json_extract(condition_json, '$.task_type') = ?
  AND json_extract(condition_json, '$.risk_level') = ?
ORDER BY 
  CASE WHEN project_pattern IS NOT NULL THEN 0 ELSE 1 END,
  confidence DESC
LIMIT 1;
```

---

## Project-Specific Overrides

### File Location

```
<project>/.universal-mwp/preferences.local.yaml
```

### Format

```yaml
# Project-specific preference overrides
# These take precedence over universal rules

overrides:
  - rule_id: auto-approve-medium-features
    action: disable
    reason: "Enterprise compliance requires all changes reviewed"
  
  - condition:
      task_type: feature
      risk_level: low
    action: auto_approve
    reason: "Personal project, auto-approve low-risk features"

project_context:
  type: enterprise_dotnet
  compliance: soc2
  team_size: 5
```

---

## File Structure After Migration

### Global (User-Level)

```
~/.ai-context/
├── universal-ai-context-patterns/     # Engine (read-only)
│   ├── IDENTITY.md
│   ├── CONTEXT.md
│   ├── pipelines/
│   ├── prompts/
│   ├── conventions/
│   ├── references/
│   └── templates/
│
└── memory/                            # Universal memory (read-write)
    ├── icm/
    │   ├── preferences.db
    │   └── embeddings/
    └── templates/
        └── preferences.local.yaml
```

### Per-Project

```
<project>/.universal-mwp/
├── context/                           # Current task state
│   ├── active-context.md
│   ├── progress.md
│   ├── tech-context.md
│   └── product-context.md
├── queue/                             # Tasks and approvals
│   ├── inbox.md
│   └── approvals.md
├── protocol/                          # Execution rules
│   ├── tick-contract.md
│   └── icm-protocol.md
├── policy/
│   └── local-tick.yaml
├── preferences.local.yaml             # Project-specific overrides (optional)
├── REQUIREMENTS.md
└── STANDARDS.json
```

### Removed from Per-Project

- `icm/preference-signals.json` → moved to universal DB
- `icm/preference-rules.yaml` → moved to universal DB
- `icm/decision-log.md` → moved to universal DB
- `icm/` folder → no longer needed

---

## Migration Path

### Phase 1: Create Universal Location

1. Create `~/.ai-context/memory/` directory structure
2. Initialize `preferences.db` with schema
3. Keep per-project `icm/` intact (dual-write period)

### Phase 2: Migrate Existing Data

```bash
# For each project with existing icm/ data
for project in $(find ~ -name ".universal-mwp" -type d); do
  migrate-to-universal "$project"
done
```

### Phase 3: Update Engine

1. Modify `tick-contract.md` to read from universal location
2. Update ICM protocol to write to universal DB
3. Add project-pattern matching to rule resolution

### Phase 4: Cleanup

1. Remove `icm/` from per-project `.universal-mwp/`
2. Update templates
3. Archive migration scripts

---

## API Specification

### Record Signal

```python
def record_signal(
    project_path: str,
    task_id: str,
    task_type: str,
    risk_level: str,
    action: str,
    context: dict = None
) -> int:
    """
    Record a preference signal from a user decision.
    Writes to ~/.ai-context/memory/icm/preferences.db
    """
    db_path = Path.home() / ".ai-context" / "memory" / "icm" / "preferences.db"
    # ... implementation
```

### Get Preference

```python
def get_preference(
    project_path: str,
    task_type: str,
    risk_level: str
) -> PreferenceResult:
    """
    Resolve preference rule for a task classification.
    
    Resolution order:
    1. Project-specific overrides (preferences.local.yaml)
    2. Project-pattern rules (from universal DB)
    3. Universal rules (from universal DB)
    4. Defaults
    """
    # ... implementation
```

---

## Benefits Summary

| Aspect | Before (Per-Project) | After (Universal) |
|--------|---------------------|-------------------|
| Learning scope | Single project | All projects |
| Repository footprint | `icm/` folder each | None (user-level) |
| Rule reusability | Manual copy | Automatic |
| Query capability | Parse JSON/YAML | SQL queries |
| Analytics | Script-based | SQL + vectors |
| Project-specific needs | Separate rules | Override layer |
| Git noise | YAML/JSON churn | None |
| Backup scope | Per-project | Single directory |

---

## Compatibility with Existing Convention

This specification extends the established `~/.ai-context/` convention:

| Existing | New |
|----------|-----|
| `~/.ai-context/universal-ai-context-patterns/` (engine) | `~/.ai-context/memory/` (memory) |
| Read-only, shared across tools | Read-write, shared across tools |
| Installed once | Populated over time |
| Tool-agnostic | Tool-agnostic |

The universal memory location follows the same principles:
- User-level, not project-level
- Shared across all wired AI tools
- Gitignored by convention (user home, not project)
- Portable (single directory for backup)

---

## Implementation Checklist

See [Universal Memory Implementation Changes](universal-memory-implementation.md) for the exact
instruction text changes to `tick-contract.md`, `icm-protocol.md`, and `install/INSTALL.md`.

- [ ] Create `~/.ai-context/memory/` structure (install + lazy creation on tick)
- [ ] Implement SQLite schema (including `pending_review`, `is_permanent`, `meta` table)
- [ ] Build daily archive process (SQLite → monthly Parquet)
- [ ] Build rule review flagging logic
- [ ] Build migration from per-project JSON/YAML to SQLite
- [ ] Apply instruction changes from `universal-memory-implementation.md` to `tick-contract.md`
- [ ] Apply instruction changes from `universal-memory-implementation.md` to `icm-protocol.md`
- [ ] Apply install step from `universal-memory-implementation.md` to `install/INSTALL.md`
- [ ] Create `preferences.local.yaml` template
- [ ] Document DuckDB as optional analytics dependency
- [ ] Test migration on existing projects
- [ ] Remove per-project `icm/` after validation

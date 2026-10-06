# Show Learned Preferences

Display learned preference rules from ICM.

## Usage

Copy and follow these steps:

## Step 1: Read Preference Rules

Query `MEMORY_HOME/icm/preferences.db` for active rules:

```sql
SELECT rule_id, project_pattern, condition_json, action, confidence,
       signal_count, last_applied_at
FROM rules
WHERE is_active = 1
ORDER BY confidence DESC;
```

Also check `.universal-mwp/preferences.local.yaml` for project-specific overrides.

## Step 2: Read Recent Signals

Query recent signals from universal memory:

```sql
SELECT task_type, risk_level, action, created_at, context_json
FROM signals
WHERE project_path = '<workspace>'
ORDER BY created_at DESC
LIMIT 20;
```

## Step 3: Format Output

```
Learned Preferences

## Derived Rules

1. {condition} → {action} (confidence: {N}%)
   - Triggered N times

## Manual Rules

- {custom rules}

## Recent Signals

- {signal history}
```

## Step 4: Suggest Actions

If rules suggest:
- High-confidence auto-approvals: suggest `/auto-approve`
- Pattern deviations: note for review

## No Output Files Modified

This is a read-only operation.
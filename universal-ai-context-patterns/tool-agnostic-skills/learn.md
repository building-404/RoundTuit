# Show Learned Preferences

Display learned preference rules from ICM.

## Usage

Copy and follow these steps:

## Step 1: Read Preference Rules

Read `.universal-mwp/icm/preference-rules.yaml`:

```yaml
# Preference Rules

## Derived Rules

rules:
  - condition: "{feature + medium}"
    action: "auto_approve"
    confidence: 0.85

## Manual Rules

- none | custom rules

## Decision Log

See signals/ for raw decision logs
```

## Step 2: Read Recent Signals

Read `.universal-mwp/icm/signals/*.md` for recent signals.

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
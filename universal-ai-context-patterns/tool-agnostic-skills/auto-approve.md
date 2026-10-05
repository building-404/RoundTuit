# Auto-Approve Tasks

Auto-approve low-risk tasks from the approvals queue, per the scope-based
risk policy.

## Usage

Copy and follow these steps:

## Step 1: Read Policy

Read `.universal-mwp/policy/local-tick.yaml`. Under the scope-based model, a
task is auto-approvable when its `change_scope` maps to a rule whose `risk` is
`low` and whose gate has `auto_execute: true` (typically `read-only` and
`new-file`).

## Step 2: Read Approvals

Read `.universal-mwp/queue/approvals.md` for pending tasks.

## Step 3: Identify Low-Risk Tasks

For each pending task, determine its `change_scope` and match it against
`risk_rules`. Select those that resolve to `risk: low`.

Also apply any `confidence >= 0.8` rule in `preference-rules.yaml` that permits
auto-approval for the task's pattern (e.g. `rule-readonly-review-is-low`).

## Step 4: Mark Approved

For each matching task:
- Move from "Pending" to "Approved" section
- Add timestamp

## Step 5: Log Signal (ICM)

Follow `protocol/icm-protocol.md`. Append one signal to
`.universal-mwp/icm/preference-signals.json` (`signals[]`):

```json
{
  "id": "sig-NNN",
  "date": "YYYY-MM-DD",
  "task": "auto-approve batch",
  "observation": "Auto-approved {N} low-risk task(s): {IDs}.",
  "signal_type": "approval_granted",
  "dimensions": { "task_type": "auto-approve", "risk_assigned": "low", "count": {N} }
}
```

Then derive/update a rule if 3+ consistent signals now exist for the pattern,
and record the decision in `icm/decision-log.md`.

## Output

```
Auto-approved {N} tasks: {IDs}
```

## Files Modified

- `.universal-mwp/queue/approvals.md`
- `.universal-mwp/icm/preference-signals.json`
- `.universal-mwp/icm/preference-rules.yaml` (only if a rule was derived/updated)
- `.universal-mwp/icm/decision-log.md`
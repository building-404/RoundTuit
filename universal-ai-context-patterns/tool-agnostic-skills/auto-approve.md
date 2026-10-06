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

Also apply any `confidence >= 0.8` rule in the universal rules table that permits
auto-approval for the task's pattern (e.g. `rule-readonly-review-is-low`).

## Step 4: Mark Approved

For each matching task:
- Move from "Pending" to "Approved" section
- Add timestamp

## Step 5: Log Signal (ICM)

Follow `protocol/icm-protocol.md`. INSERT one signal into
`MEMORY_HOME/icm/preferences.db` (signals table):

```sql
INSERT INTO signals (project_path, project_name, task_id, task_type,
  risk_level, action, confidence, context_json)
VALUES ('<workspace>', '<project>', 'auto-approve-batch', 'auto-approve', 'low',
  'approved', 1.0,
  '{"observation": "Auto-approved {N} low-risk task(s): {IDs}.",
    "signal_type": "approval_granted",
    "dimensions": {"task_type": "auto-approve", "risk_assigned": "low", "count": {N}}}');
```

Then derive/update a rule if 3+ consistent signals now exist for the pattern,
and record the decision in the decisions table.

## Output

```
Auto-approved {N} tasks: {IDs}
```

## Files Modified

- `.universal-mwp/queue/approvals.md`
- `MEMORY_HOME/icm/preferences.db` (signals + rules + decisions tables)
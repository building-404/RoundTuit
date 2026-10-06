# Approve Task

Approve a pending task from the approvals queue.

## Usage

`/approve [TASK_ID]` — or follow steps below:

## Step 1: Read Approvals

Read `.universal-mwp/queue/approvals.md`:

```markdown
## Pending Approvals

- [ ] P{0-3} {ID} | title: {description} | status: pending
```

## Step 2: Identify Task

- If TASK_ID provided: find that specific task
- If no TASK_ID: use the most recent pending task

## Step 3: Mark Approved

Move task from "Pending" to "Approved" section:

```markdown
## Approved

| {ID} | {description} | risk: {level} | {date} |
```

## Step 4: Log Signal (ICM)

Follow `protocol/icm-protocol.md`. INSERT a signal into
`MEMORY_HOME/icm/preferences.db` (signals table):

```sql
INSERT INTO signals (project_path, project_name, task_id, task_type,
  risk_level, action, confidence, context_json)
VALUES ('<workspace>', '<project>', '{ID}', '{type}', '{level}',
  'approved', 1.0,
  '{"observation": "User approved {ID} ({title}).",
    "signal_type": "approval_granted",
    "dimensions": {"task_type": "{type}", "risk_assigned": "{level}"}}');
```

Then per the protocol, derive/update a rule in the rules table if this
signal is a persistent correction/guardrail, or if 3+ consistent signals now
exist for this pattern. Record the decision in the decisions table.

## Step 5: Confirm

```
Approved: {ID} - {title}
```

## Files Modified

- `.universal-mwp/queue/approvals.md`
- `MEMORY_HOME/icm/preferences.db` (signals + rules + decisions tables)
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

Follow `protocol/icm-protocol.md`. Append a signal to
`.universal-mwp/icm/preference-signals.json` (`signals[]`):

```json
{
  "id": "sig-NNN",
  "date": "YYYY-MM-DD",
  "task": "{ID}",
  "observation": "User approved {ID} ({title}).",
  "signal_type": "approval_granted",
  "dimensions": { "task_type": "{type}", "risk_assigned": "{level}" }
}
```

Then per the protocol, derive/update a rule in `preference-rules.yaml` if this
signal is a persistent correction/guardrail, or if 3+ consistent signals now
exist for this pattern. Record the decision in `icm/decision-log.md`.

## Step 5: Confirm

```
Approved: {ID} - {title}
```

## Files Modified

- `.universal-mwp/queue/approvals.md`
- `.universal-mwp/icm/preference-signals.json`
- `.universal-mwp/icm/preference-rules.yaml` (only if a rule was derived/updated)
- `.universal-mwp/icm/decision-log.md`
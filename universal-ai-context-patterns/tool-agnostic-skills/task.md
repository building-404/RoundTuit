# Add Task

Add a new task to the inbox.

## Usage

Copy and follow these steps:

## Step 1: Parse Task Input

From user input, extract:
- **Priority**: P0, P1, P2, or P3 (default: P2)
- **Task ID**: e.g., DEV-123, IMP-001
- **Title**: description after `|`

Format: `/task [PRIORITY] [TASK_ID] | [TITLE]`

## Step 2: Validate Priority

| Priority | Risk Level |
|----------|------------|
| P0 | Critical |
| P1 | High |
| P2 | Medium (default) |
| P3 | Low |

## Step 3: Read Current Queue

Read `.universal-mwp/queue/inbox.md`:

```markdown
## Queue

- [ ] P{0-3} {ID} | title: {description} | status: pending

## Recently Completed

- {previous tasks}
```

## Step 4: Append New Task

Append to "Queue" section:

```markdown
- [ ] P{0-3} {ID} | title: {TITLE} | status: pending
```

## Step 5: Confirm

```
Task added to queue (position {N} of {N}):

- [ ] P{0-3} {ID} | title: {TITLE} | status: pending
```

## Files Modified

- `.universal-mwp/queue/inbox.md`
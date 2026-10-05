# Show Inbox

Display pending tasks from the queue.

## Usage

Copy and follow these steps:

## Step 1: Read Queue

Read `.universal-mwp/queue/inbox.md`:

```markdown
## Queue

- [ ] P{0-3} {ID} | title: {description} | status: pending
...

## Recently Completed

- {completed tasks}
```

## Step 2: Count Tasks

- **Pending**: N tasks in Queue section
- **Completed**: N tasks in Recently Completed section

## Step 3: Format Output

```
Inbox ({N} pending, {M} completed)

## Queue

1. [P{0-3}] {ID} | {title}
...

## Recently Completed

- {previous}
```

## No Output Files Modified

This is a read-only operation.
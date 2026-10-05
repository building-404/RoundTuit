# Show Status

Display current project status from context files.

## Usage

Copy and follow these steps:

## Step 1: Read Active Context

Read `.universal-mwp/context/active-context.md`:

```markdown
## Current Task

- **ID**: {TASK_ID}
- **Title**: {TITLE}
- **Priority**: P{0-3}
- **Status**: {In Progress|Pending|Complete}
- **Stage**: {stage name}
```

## Step 2: Read Progress

Read `.universal-mwp/context/progress.md`:

```markdown
## Milestones

- {date}: {TASK_ID} complete - {description}
```

## Step 3: Read Approvals

Read `.universal-mwp/queue/approvals.md`:

```markdown
## Pending Approvals

*No pending approvals* | or list

## Approved

*None yet* | or list
```

## Step 4: Read Inbox

Read `.universal-mwp/queue/inbox.md` for queue count.

## Step 5: Format Output

```
Status Report

- Current Task: {ID} - {TITLE} ({status})
- Last Action: {recent action}
- Pending Approvals: {N}
- Recently Completed:
  - {tasks}
- Blocked: {none | items}
```

## No Output Files Modified

This is a read-only operation.
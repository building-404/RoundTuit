# Complete Task

Mark the current task complete and clear active context.

## Usage

Copy and follow these steps:

## Step 1: Read Current Context

Read `.universal-mwp/context/active-context.md`:

```
ID: {TASK_ID}
Title: {TASK_TITLE}
```

## Step 2: Log to Progress

Read `.universal-mwp/context/progress.md`, append:

```
- {date}: {TASK_ID} complete - {TASK_TITLE}
```

## Step 3: Update Queue

Read `.universal-mwp/queue/inbox.md`:
- Mark task complete
- Move to "Recently Completed"

## Step 4: Log Signal (ICM)

Per `protocol/icm-protocol.md`, if completing the task involved a user
decision worth learning (a correction, standing instruction, or notable
approval), INSERT a signal into `MEMORY_HOME/icm/preferences.db` and
update the rules/decisions tables as the protocol directs.
Routine completions with no new user decision do not need a signal.

Note: `rule-complete-when-done` means finished work should be marked complete
immediately rather than pausing to ask — apply it here.

## Step 5: Clear Active Context

Write to `.universal-mwp/context/active-context.md`:

```markdown
# Active Context

Current task being actively worked on.

*No active task*
```

## Output

```
{TASK_ID} complete. Active context cleared.
```

## Files Modified

- `.universal-mwp/context/active-context.md`
- `.universal-mwp/context/progress.md`
- `.universal-mwp/queue/inbox.md`
- `MEMORY_HOME/icm/preferences.db` (only if a signal/rule was logged)
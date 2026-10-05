# Approve PR

Approve and publish a PR draft via GitHub CLI.

## Usage

`/approve-pr {PR_ID}` — or follow steps below:

## Step 1: Read PR Draft

Read `.universal-mwp/queue/pr-drafts.md`:

```markdown
| PR # | Title | Status | Revisions |
| {ID} | {title} | draft | {N} |
```

## Step 2: Verify Readiness

Check:
- All commits are approved and applied
- Revisions are complete
- PR body is finalized

## Step 3: Publish via gh CLI

Run:

```bash
# Create PR (if new)
gh pr create --title "{title}" --body-file pr-body.md --base main --head {branch}

# Or update existing draft
gh pr edit {pr_number} --title "{title}" --body-file revised.md
```

## Step 4: Update Draft Queue

Edit `.universal-mwp/queue/pr-drafts.md`:

```markdown
| {PR#} | {title} | published | {revisions} |
```

## Step 5: Log Progress

Read `.universal-mwp/context/progress.md`, append:

```
- {date}: PR #{PR#} published - {title}
```

## Output

```
PR #{PR#} published - https://github.com/{owner}/{repo}/pull/{PR#}
```

## Files Modified

- `.universal-mwp/queue/pr-drafts.md`
- `.universal-mwp/context/progress.md`

## gh CLI Commands

- `gh pr create --title "..." --body-file ... --base main` — create new PR
- `gh pr edit {pr_number} --title "..." --body-file ...` — edit PR
- `gh pr view {pr_number} --json number,title,state,url` — get PR details
- `gh pr status` — show current branch PR status
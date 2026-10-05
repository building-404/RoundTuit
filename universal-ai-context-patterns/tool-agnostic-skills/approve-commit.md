# Approve Commit

Approve and apply a staged commit.

## Usage

`/approve-commit {COMMIT_ID}` — or follow steps below:

## Step 1: Read Pending Commit

Read `.universal-mwp/commit-review/pending-commits/{commit-id}.md`:

```
Message: {commit message}
Files: {list}
Diff: {unified diff}
```

## Step 2: Review

Review the commit content. If acceptable:

## Step 3: Update Approvals

Read `.universal-mwp/commit-review/approvals.md`:

- Move commit from "Pending" to "Approved"
- Add SHA placeholder: `pending-git-commit`

## Step 4: Apply Commit

Run:

```bash
git add {files}
git commit -m "{commit message}"
```

## Step 5: Update Approvals with SHA

Edit `.universal-mwp/commit-review/approvals.md`:

```markdown
| {SHA} | {message} | approved | applied |
```

## Step 6: Update Metadata

Read `.universal-mwp/commit-review/meta/workflow.yaml`:

```yaml
approved: {N}
applied: {M}
```

## Output

```
Commit {SHA} applied.
```

## Files Modified

- `.universal-mwp/commit-review/pending-commits/{id}.md`
- `.universal-mwp/commit-review/approvals.md`
- `.universal-mwp/commit-review/meta/workflow.yaml`

## Git Commands

- `git add {files}` — stage changes
- `git commit -m "{msg}"` — commit with message
- `git log -1 --format="%H"` — get SHA of last commit
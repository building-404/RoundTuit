# Universal AI Context Patterns — Kiro Entry Point (Global)

This steering file is auto-loaded by Kiro. It points to the shared
**universal-ai-context-patterns** engine plus the per-project state that lives in
each workspace.

The **engine** (project-agnostic) lives at `{{ENGINE_HOME}}`.
The **state** (per-project) lives at `<workspace-root>/.universal-mwp/`.

---

## Start Here

1. **Read `{{ENGINE_HOME}}/IDENTITY.md`** — workspace map (Layer 0)
2. **Read `{{ENGINE_HOME}}/CONTEXT.md`** — task routing (Layer 1)
3. **Read `<workspace-root>/.universal-mwp/protocol/tick-contract.md`** — execution rules
   (if absent, this is a new project — proceed to intake per CONTEXT.md)

---

## New Project? Initialize State First

If `<workspace-root>/.universal-mwp/` does not exist, this workspace has not been
initialized. Treat every state read below as optional: if a file is missing, skip
it — never hard-fail. On the first task, seed the `.universal-mwp/` skeleton by
copying `{{ENGINE_HOME}}/templates/universal-mwp/` into
`<workspace-root>/.universal-mwp/`, then fill in project-specific values
(project name, workspace path, tech/product context). Do NOT hand-author these
defaults from memory — the template is the source of truth and stays current
with the latest proven policy/ICM/conventions.

---

## Engine Reference (global)

| What | Where |
|------|-------|
| Workspace map | `{{ENGINE_HOME}}/IDENTITY.md` |
| Task routing | `{{ENGINE_HOME}}/CONTEXT.md` |
| Pipeline stages | `{{ENGINE_HOME}}/pipelines/01-research.md` → `05-proof-of-concept.md` |
| Workflow prompts | `{{ENGINE_HOME}}/prompts/*.md` |
| Conventions | `{{ENGINE_HOME}}/conventions/*.md` |
| References | `{{ENGINE_HOME}}/references/*.md` |

## State Reference (per-project, workspace-relative)

| What | Where |
|------|-------|
| Execution rules | `<workspace-root>/.universal-mwp/protocol/tick-contract.md` |
| Current task | `<workspace-root>/.universal-mwp/context/active-context.md` |
| Progress | `<workspace-root>/.universal-mwp/context/progress.md` |
| Pending tasks | `<workspace-root>/.universal-mwp/queue/inbox.md` |
| Approvals | `<workspace-root>/.universal-mwp/queue/approvals.md` |
| Preference rules | `<workspace-root>/.universal-mwp/icm/preference-rules.yaml` |
| Risk policy | `<workspace-root>/.universal-mwp/policy/local-tick.yaml` |
| Outputs | `<workspace-root>/.universal-mwp/OUTPUT/` |

All run state and artifacts live in the workspace's own `.universal-mwp/` folder.
Before writing any file, ensure its parent directory exists — never fail because
a path doesn't exist yet.

---

## Slash Commands (skills)

| Command | Purpose |
|---------|---------|
| `/inbox` | Show pending tasks |
| `/task P{0-3} {ID} | {title}` | Add a task to the inbox |
| `/status` | Show project status |
| `/complete` | Mark current task complete, clear context |
| `/approvals` | Show pending approvals |
| `/approve [TASK_ID]` | Approve a pending task |
| `/auto-approve` | Auto-approve low-risk tasks per policy |
| `/approve-commit {COMMIT_ID}` | Approve and apply a staged commit |
| `/approve-pr {PR_ID}` | Approve and publish a PR draft (gh CLI) |
| `/learn` | Show learned preference rules |

Each Kiro skill is a thin wrapper over the DRY instructions in
`{{ENGINE_HOME}}/tool-agnostic-skills/`.

---

## Kiro-Specific Notes

### Knowledge Tool Integration

Index preference rules for querying:

```bash
kiro-cli knowledge add \
  --name mwp-preference-rules \
  --value file://.universal-mwp/icm/preference-rules.yaml
```

Query before classification:
```
knowledge search --query "task_type:feature risk:medium"
```

### ICM Learning Protocol

Signal → rule mechanics are defined canonically in
`<workspace-root>/.universal-mwp/protocol/icm-protocol.md`; the tick flow is in
`<workspace-root>/.universal-mwp/protocol/tick-contract.md`.

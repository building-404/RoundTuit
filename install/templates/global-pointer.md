# Universal AI Context Patterns — Global Pointer

This is global, user-level context. It is **not** committed to any project. It points
every AI coding assistant at the shared, tool-agnostic engine and confines all
per-project state to a single gitignored folder.

## Engine (shared, global)

The engine lives at:

```
{{ENGINE_HOME}}
```

When a task begins, load in this order:

1. `{{ENGINE_HOME}}/IDENTITY.md` — workspace map (Layer 0)
2. `{{ENGINE_HOME}}/CONTEXT.md` — task routing (Layer 1)
3. `{{ENGINE_HOME}}/pipelines/*.md` — numbered stage files, as routed
4. `{{ENGINE_HOME}}/prompts/*.md` — executable workflow prompts (new/update .NET,
   content pipeline, clean-code review)
5. `{{ENGINE_HOME}}/conventions/*.md` and `{{ENGINE_HOME}}/references/*.md` — as needed

## State (per-project, gitignored)

All run state and outputs live **only** in the workspace's own `.universal-mwp/`
folder, which is gitignored and does not ship with the project:

```
<workspace-root>/.universal-mwp/
├── protocol/tick-contract.md   # execution rules
├── context/                    # session state
├── queue/                      # inbox.md, approvals.md
├── icm/                        # preference learning
├── policy/local-tick.yaml      # risk classification
└── OUTPUT/                     # generated artifacts
```

If `.universal-mwp/` does not exist, this is a new project: treat every state read as
optional (never hard-fail on a missing file) and create the skeleton on the first
task before writing state.

## Rules

- **Do not** create or rely on any project-committed context files (no `AGENTS.md`,
  no `CLAUDE.md`, no `.github/copilot-instructions.md`, no `.cursor/rules` in the
  project). The engine is global; the only project footprint is the gitignored
  `.universal-mwp/`.
- The engine never changes between projects. All project specifics live in
  `.universal-mwp/`.
- Each invocation is one deterministic tick: pick the highest-priority pending task
  from `.universal-mwp/queue/inbox.md`, classify risk, execute if low risk or
  approved, otherwise request approval and stop.

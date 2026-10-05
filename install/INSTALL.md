# Universal AI Context Patterns — Global Install (script-free, multi-tool)

You are installing the **Universal AI Context Patterns** engine into the user's
**global** space and wiring it into every AI CLI they use — **without adding any
files to any project's source control**.

This file is an instruction set for an AI agent. It uses **no scripts** — you perform
every step with your own file read/write/copy tools. It resolves the home directory
at run time, so it is cross-platform.

## Core principle: global engine, gitignored project state

- The **engine** installs **once** to a shared, tool-neutral global home.
- Each AI tool is wired via its **global / user-level** config — never via
  project-committed files (no `AGENTS.md`, `CLAUDE.md`, `.github/`, `.cursor/` in the
  project).
- The **only** per-project footprint is `<workspace>/.universal-mwp/`, which is
  **gitignored** and created on first use. It does not ship with the project.

> Run this from the root of this repo. If you are elsewhere, ask the user for the
> repo path first.

---

## Definitions (resolve these first, state them back to the user)

1. **REPO_ROOT** — the folder containing this `install/` directory. Confirm it
   contains `universal-ai-context-patterns/`.
2. **HOME** — the user's home directory, resolved at run time:
   - Windows: `%USERPROFILE%` (e.g. `C:\Users\<name>`)
   - macOS/Linux: `$HOME`
3. **ENGINE_HOME** — the shared engine home (plain path):
   `HOME/.ai-context/universal-ai-context-patterns`
   Use forward slashes in any `file://` URI regardless of OS.
4. **ENGINE_URI** — `file://` URI for `ENGINE_HOME`
   (e.g. `file:///C:/Users/<name>/.ai-context/universal-ai-context-patterns`).
5. **KIRO_HOME_PATH** / **KIRO_HOME_URI** — `HOME/.kiro` as plain path and `file://`
   URI (used only for Kiro's agent/steering/skills).

---

## Step 1 — Install the shared engine (always)

- Ensure `ENGINE_HOME` exists (create parents as needed).
- Copy the entire contents of `REPO_ROOT/universal-ai-context-patterns/` into
  `ENGINE_HOME`, preserving structure: `IDENTITY.md`, `CONTEXT.md`, `README.md`,
  `pipelines/`, `prompts/`, `conventions/`, `references/`, and `.kiro/skills/`.
- Back up any existing `ENGINE_HOME` content you would overwrite by copying it to
  `ENGINE_HOME.bak-<yyyyMMdd-HHmmss>` first (skip if nothing exists).

This engine is now shared by every tool below.

### Engine contents (what Step 1 copies)

- `IDENTITY.md`, `CONTEXT.md`, `README.md`
- `pipelines/`, `prompts/`, `conventions/`, `references/`
- `.kiro/skills/` — Kiro slash-command wrappers
- `tool-agnostic-skills/` — the DRY source-of-truth skill instructions
  (usable by any tool: Kiro, Claude, Gemini, Copilot, Amazon Q)
- `templates/universal-mwp/` — the canonical per-project state skeleton that
  new projects are seeded from on first use (see Step 1a)

### Step 1a — Per-project skeleton is template-driven

The per-project `.universal-mwp/` folder is **no longer hand-authored with
inline defaults**. On a project's first task:

1. **Ensure `.universal-mwp/` is gitignored** (do this first):
   - Check if `<workspace>/.gitignore` exists
   - If yes, check if `.universal-mwp/` is already ignored (look for exact match or pattern that covers it)
   - If not ignored, append a newline and `.universal-mwp/` to `.gitignore`
   - If no `.gitignore` exists, create one with `.universal-mwp/` as the first entry

2. **Seed the project state folder**:
   - Copy `ENGINE_HOME/templates/universal-mwp/` into `<workspace>/.universal-mwp/`
   - Fill in project-specific values (project name, workspace path, tech/product context)

The skeleton includes:

- `protocol/tick-contract.md`, `protocol/icm-protocol.md`
- `policy/local-tick.yaml` (scope-based risk model)
- `icm/preference-rules.yaml` (seeded rules), `icm/preference-signals.json`
  (empty `preference-signals@1`), `icm/decision-log.md`
- `context/active-context.md`, `progress.md`, `tech-context.md`, `product-context.md`
- `queue/inbox.md`, `queue/approvals.md`
- `conventions/pr-review.md`
- `reviews/README.md`, `archived/README.md`

This keeps every new install current with the latest proven defaults; do not
re-derive these files from memory.

---

## Step 2 — Detect which tools to wire

Ask the user which of these AI CLIs they want wired (or detect by checking whether the
home dir exists). Only wire the ones they use:

| Tool | Detect (global home) | Wire target (global, user-level) |
|------|----------------------|----------------------------------|
| Kiro CLI | `HOME/.kiro/` | agent + steering + skills (Step 3) |
| Claude Code | `HOME/.claude/` | `HOME/.claude/CLAUDE.md` |
| Gemini CLI | `HOME/.gemini/` | `HOME/.gemini/GEMINI.md` |
| GitHub Copilot CLI | Copilot user config dir | user-level custom instructions |
| Amazon Q | `HOME/.aws/amazonq/` | `HOME/.aws/amazonq/global_context` memory |

For every tool wired in Steps 3–4, first back up any existing target file to
`<target>.bak-<timestamp>`.

---

## Step 3 — Wire Kiro CLI (if used)

1. Render `install/templates/mwp-protocol.md`:
   - Replace `{{ENGINE_HOME}}` → `ENGINE_HOME` (plain path).
   - Write to `HOME/.kiro/steering/mwp-protocol.md`.
2. Render `install/templates/mwp-agent.json`:
   - Replace `{{ENGINE_URI}}` → `ENGINE_URI`.
   - Replace `{{KIRO_HOME_URI}}` → `KIRO_HOME_URI`.
   - Replace `{{KIRO_HOME_PATH}}` → `KIRO_HOME_PATH`.
   - Write to `HOME/.kiro/agents/mwp-agent.json` as UTF-8 **without a BOM**.
3. Copy skills: for each folder under
   `REPO_ROOT/universal-ai-context-patterns/.kiro/skills/`
   (`task`, `status`, `learn`, `inbox`, `approve`, `approvals`), copy its `SKILL.md`
   to `HOME/.kiro/skills/<name>/SKILL.md`.
4. Validate:
   - `kiro-cli agent validate --path <HOME>/.kiro/agents/mwp-agent.json`
   - `kiro-cli agent list` → confirm `mwp-agent` appears as **Global**.

> Note: `HOME/.kiro/steering/mwp-protocol.md` auto-loads into Kiro's default agent in
> every session. If the user does not want that, skip writing the steering file — the
> `mwp-agent` still loads it via its own `resources`.

---

## Step 4 — Wire the other tools (each, if used)

All of these use the **same** shared global pointer, rendered from
`install/templates/global-pointer.md`:

1. Read `install/templates/global-pointer.md`.
2. Replace every `{{ENGINE_HOME}}` token with `ENGINE_HOME` (plain path).
3. Write the rendered content to each selected tool's global target:
   - **Claude Code** → `HOME/.claude/CLAUDE.md`
   - **Gemini CLI** → `HOME/.gemini/GEMINI.md`
   - **GitHub Copilot CLI** → the user-level custom-instructions file for the
     installed Copilot CLI version. If you cannot confirm the exact path, ask the
     user rather than guessing.
   - **Amazon Q** → `HOME/.aws/amazonq/global_context` (global memory). If the exact
     mechanism differs on the installed version, ask the user.

If a target file already exists with unrelated content, do **not** clobber it: append
the rendered pointer under a clear `# Universal AI Context Patterns` heading (after
backing up), or ask the user how to merge.

---

## Step 5 — Report

Summarize:
- `ENGINE_HOME` path and what was copied.
- Each tool wired and the exact file written.
- Anything backed up (`.bak-<timestamp>`).
- How to use per tool:
  - Kiro: `kiro-cli chat --agent mwp-agent`
  - Claude / Gemini / Copilot / Amazon Q: just start a session — the global pointer
    loads automatically.
- Reminder: the only per-project footprint is the gitignored `.universal-mwp/`,
  created on first task.

---

## Notes

- **No project-committed files.** Everything is global/user-level. The engine is
  shared; project state is confined to the gitignored `.universal-mwp/`.
- **No hardcoded user paths.** Every path derives from the resolved `HOME`. Templates
  carry only `{{ENGINE_HOME}}`, `{{ENGINE_URI}}`, and `{{KIRO_HOME_*}}` tokens.
- **Encoding.** Write `mwp-agent.json` as UTF-8 **without a BOM** (a leading BOM makes
  Kiro's JSON parser fail with "expected value at line 1 column 1").
- **Re-running is safe.** Existing targets are backed up before overwrite.
- **Per-project state** (`.universal-mwp/`) is created on first task, not by this
  installer.

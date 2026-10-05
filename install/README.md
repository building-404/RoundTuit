# Global Install (script-free, multi-tool)

Install the **Universal AI Context Patterns** engine once into a shared global
location and wire it into every AI CLI you use — **with no scripts** and **no files
added to any project's source control**.

## Design

- **One shared engine**, installed to `~/.ai-context/universal-ai-context-patterns/`.
- **Each tool wired via its global/user-level config** — never project-committed
  files.
- **The only per-project footprint** is `<workspace>/.universal-mwp/`, which is
  **gitignored** and created on first use.

## What gets installed

| Location | Contents |
|----------|----------|
| `~/.ai-context/universal-ai-context-patterns/` | The shared engine (IDENTITY, CONTEXT, pipelines, prompts, conventions, references, skills) |
| `~/.kiro/steering/mwp-protocol.md` | Kiro entry point (points at the shared engine) |
| `~/.kiro/agents/mwp-agent.json` | The Kiro `mwp-agent` |
| `~/.kiro/skills/` | Kiro slash-command skills |
| `~/.claude/CLAUDE.md` | Claude Code global pointer (if wired) |
| `~/.gemini/GEMINI.md` | Gemini CLI global pointer (if wired) |
| Copilot CLI user instructions | GitHub Copilot global pointer (if wired) |
| `~/.aws/amazonq/global_context` | Amazon Q global pointer (if wired) |

## How to install

1. Open this repo in any AI CLI with filesystem access. Example with Kiro:
   ```
   kiro-cli chat
   ```
2. Tell the agent:
   ```
   Run install/INSTALL.md
   ```
   The agent resolves your home directory, installs the shared engine, asks which
   tools to wire, renders each tool's global pointer, backs up anything it would
   overwrite, and validates the Kiro agent.

No `.ps1`, no `.sh`, cross-platform.

## After install

- **Kiro**: `kiro-cli chat --agent mwp-agent`
- **Claude / Gemini / Copilot / Amazon Q**: just start a session — the global pointer
  loads automatically and directs the assistant to the shared engine.

## Files in this folder

| File | Purpose |
|------|---------|
| `INSTALL.md` | Agent-runnable, multi-tool install instructions |
| `templates/mwp-protocol.md` | Kiro steering entry point (`{{ENGINE_HOME}}` token) |
| `templates/mwp-agent.json` | Kiro agent config (`{{ENGINE_URI}}`, `{{KIRO_HOME_*}}` tokens) |
| `templates/global-pointer.md` | Shared global pointer for Claude / Gemini / Copilot / Amazon Q (`{{ENGINE_HOME}}` token) |

## Notes

- **No project-committed files.** The engine is global; project state is confined to
  the gitignored `.universal-mwp/`.
- **Re-running is safe**: existing targets are backed up (`.bak-<timestamp>`).
- `~/.kiro/steering/mwp-protocol.md` auto-loads into Kiro's default agent in every
  session. Skip that step during install if you don't want it — the `mwp-agent` still
  loads the engine via its own `resources`.

# Universal AI Context Patterns

A self-contained, tool-agnostic engine for driving AI coding assistants through
structured context: layered routing, numbered pipeline stages, executable workflow
prompts, coding conventions, and a preference-learning (ICM) tick protocol.

It is designed to be installed once into a shared location and pointed at from any
AI CLI — Kiro CLI, GitHub Copilot, Claude Code, Cursor, Gemini CLI, Codex, and any
tool that reads `AGENTS.md`.

---

## Structure

```
universal-ai-context-patterns/
├── IDENTITY.md          # Layer 0 — workspace map ("Where am I?")
├── CONTEXT.md           # Layer 1 — task routing ("Where do I go?")
├── pipelines/           # Layer 2 — numbered stage files
│   ├── 01-research.md
│   ├── 02-structuring.md
│   ├── 03-code-generation.md
│   ├── 04-documentation.md
│   └── 05-proof-of-concept.md
├── prompts/             # Executable workflow prompts
│   ├── new-dotnet-api.md
│   ├── update-dotnet-api.md
│   ├── content-pipeline.md
│   ├── business-process-modernization.md
│   └── clean-code-review.md
├── conventions/         # Coding + workflow standards
│   ├── dotnet.md
│   ├── post-execution.md
│   └── tool-compatibility.md
├── references/          # Stable reference material
│   ├── conventions.md
│   ├── glossary.md
│   ├── voice.md
│   ├── rate-limiting.md
│   └── refactoring.md
└── .kiro/skills/        # Slash-command skills (task, status, inbox, ...)
```

Per-project run state lives in each workspace's own `.universal-mwp/` folder
(created on first use), never inside this engine.

---

## Reading Order

1. **IDENTITY.md** — workspace map
2. **CONTEXT.md** — task routing
3. **`<workspace-root>/.universal-mwp/protocol/tick-contract.md`** — execution rules
4. **Workflow prompt, then its stage files** — for the current task

Workflow prompts define end-to-end workflows; numbered pipeline files provide reusable stages used by workflows.

---

## Install

Do not copy this folder by hand. Use the script-free installer, which deploys the
engine to a shared location and wires up each AI tool via its native convention:

```
kiro-cli chat
> Run install/INSTALL.md
```

See [`../install/README.md`](../install/README.md).

---

## Principles

- **Self-contained**: no references outside this folder; the engine never changes
  between projects.
- **Tool-agnostic**: plain markdown/yaml/json; deployed via each tool's own context
  mechanism.
- **File-native state**: all run state is inspectable plain text under
  `.universal-mwp/` — the filesystem is the state machine.

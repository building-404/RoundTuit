# RoundTuit

**Repetitive Operational Unit for Nested Development: Text-Unit Iterative Tracker**

AI chat is powerful but incomplete. It lacks the persistent structures that make human developers effective: memory across sessions, learned preferences, structured workflows, and state that survives context limits.

RoundTuit gives AI chat the missing pieces of a brain it needs to complete your request and *get RoundTuit* — working memory, long-term memory, task management, and repeatable processes encoded as files rather than code.

## What It Provides

A tool-agnostic, Markdown-native framework for repeatable AI workflows: research,
content creation, and software development. Its processes are encoded as staged
instructions, context files, and filesystem state rather than a separate orchestration
runtime. It runs in AI tools with filesystem access — no server, VM, or cron required.

## Design Lineage

ICM is a published way of organizing agent work through folders and staged context,
first known as **Model Workspace Protocol (MWP)** in [Jake Van Clief and David McDermott's
research paper](https://arxiv.org/abs/2603.16021).

This project is a workflow-specific implementation of ICM, not a canonical framework.
MWP remains the project's protocol lineage and the name used for per-project state
(`.universal-mwp/`), while ICM describes the structural method. The tick protocol,
workflow pipelines, and preference-learning behavior are this project's extensions
around that method.

Each chat invocation is one deterministic tick. State persists across sessions via
local files in each project's `.universal-mwp/` folder.

## How It Works

1. Install the engine once into a shared global location and wire it into your AI
   CLIs (see [Install](#install)). Works with Kiro CLI, Claude Code, Gemini CLI,
   GitHub Copilot CLI, and Amazon Q.
2. Start any wired tool — the global pointer directs it to the shared engine
   (Kiro: `kiro-cli chat --agent mwp-agent`).
3. Answer the intake questions — the system routes to the correct workflow and
   persists state in the gitignored `<your-project>/.universal-mwp/`.

## Structure

```
universal-ai-context-patterns/       # The self-contained, tool-agnostic engine
├── IDENTITY.md                      # Layer 0 — workspace map ("Where am I?")
├── CONTEXT.md                       # Layer 1 — task routing ("Where do I go?")
├── pipelines/                       # Layer 2 — numbered stage files
│   ├── 01-research.md
│   ├── 02-structuring.md
│   ├── 03-code-generation.md
│   ├── 04-documentation.md
│   └── 05-proof-of-concept.md
├── prompts/                         # Executable workflow prompts
│   ├── new-dotnet-api.md            # Greenfield .NET API (5 stages)
│   ├── update-dotnet-api.md         # Modify existing .NET API (3 stages)
│   ├── content-pipeline.md          # Research/content pipeline (5 modes)
│   ├── business-process-modernization.md # Existing process/system modernization
│   └── clean-code-review.md         # Standalone clean-code review
├── conventions/                     # Coding + workflow standards
│   ├── dotnet.md                    # SOLID principles, patterns, audit checklist
│   ├── post-execution.md            # Branch/commit/push workflow
│   └── tool-compatibility.md        # Prefer built-in AI tools over shell
├── references/                      # Stable reference material
│   ├── conventions.md
│   ├── glossary.md
│   ├── voice.md
│   ├── rate-limiting.md
│   └── refactoring.md
└── .kiro/skills/                    # Slash-command skills (task, status, inbox, ...)

install/                             # Script-free global installer
├── INSTALL.md                       # Agent-runnable install instructions
├── README.md                        # Install docs
└── templates/                       # Portable agent + steering (no hardcoded paths)
    ├── mwp-agent.json
    └── mwp-protocol.md
```

## Install

The installer is **script-free** — the AI agent performs it by following a markdown
instruction set, resolving your home directory at run time (cross-platform).

1. Open this repo in any AI CLI with filesystem access (e.g. `kiro-cli chat`)
2. Tell the agent: `Run install/INSTALL.md`

This installs the engine once to a shared global home and wires each tool via its
**global / user-level** config — **no files are added to any project's source
control**:

| Global location | Contents |
|-----------------|----------|
| `~/.ai-context/universal-ai-context-patterns/` | The shared engine (IDENTITY, CONTEXT, pipelines, prompts, conventions, references, skills) |
| `~/.kiro/` | Kiro agent + steering + skills (points at the shared engine) |
| `~/.claude/CLAUDE.md` | Claude Code global pointer (if wired) |
| `~/.gemini/GEMINI.md` | Gemini CLI global pointer (if wired) |
| Copilot CLI user instructions | GitHub Copilot global pointer (if wired) |
| `~/.aws/amazonq/global_context` | Amazon Q global pointer (if wired) |

The **only** per-project footprint is the gitignored `.universal-mwp/`.

See [`install/README.md`](install/README.md) for details.

## Manifest (per-project)

Each project you work on gets a `.universal-mwp/` folder at its workspace root,
created on first use:

```
<your-project>/.universal-mwp/
├── protocol/tick-contract.md   # Canonical execution rules
├── context/                    # Session state (progress, active task, tech/product context)
├── queue/                      # Task queue (inbox.md) and approval gates (approvals.md)
├── icm/                        # Preference learning (signals, rules, decision log)
├── policy/local-tick.yaml      # Risk classification config
├── REQUIREMENTS.md             # What to build/research
├── STANDARDS.json              # Code style guidelines
├── BRANDS.json                 # Content brand voice (content pipeline)
├── TOPICS.md                   # Research topics (content pipeline)
└── SOURCE_MATERIAL/            # Input files (content pipeline)
```

## Workflows

| Workflow | Trigger | Stages |
|----------|---------|--------|
| New .NET API | `new` | Research → Structure → Code Gen → Docs → PoC |
| Update .NET API | `update` | Research → Structure → Code Gen |
| Content | `content` | 5 modes: full, research, content, iterate, migrate |
| Business process modernization | `modernize` | Analyze → Review handoff → Design tests → Implement → Verify/adopt |
| Clean code review | `review` | Standalone Clean Code audit |

## Autonomous Tick Mode

Each invocation processes one task from `queue/inbox.md`:
- **Low risk**: executes immediately
- **Medium/High risk**: requests approval in `queue/approvals.md`, stops
- Preferences learned over time via `icm/` (signals → rules → auto-adjustments)

Slash-command skills: `/inbox`, `/task`, `/status`, `/approvals`, `/approve`, `/learn`.

### Preference Learning (ICM)

The system observes your decisions and derives rules over time:

```
1. You approve a medium-risk feature task
   → signal logged: { task_type: "feature", risk: "medium", action: "approved" }

2. After 3 similar approvals
   → rule derived: { condition: "feature + medium", action: "auto_approve", confidence: 0.85 }

3. Next feature task at medium risk
   → auto-approved per learned rule, logged in decision-log.md
```

All rules are human-editable. Delete or adjust any rule in
`icm/preference-rules.yaml` at any time.

## Principles

- The engine is self-contained and never changes between projects
- All project-specific data lives in the workspace's `.universal-mwp/`
- Each prompt is self-contained and independently referenceable
- State is plain-text and inspectable — the filesystem is the state machine

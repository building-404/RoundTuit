# ICM — Identity

> MWP-Kiro Combined Workspace — AI-assisted development with preference learning and autonomous execution

---

## Folder Map

```
your-project/
├── IDENTITY.md                    # Layer 0 — you are here
├── CONTEXT.md                     # Layer 1 — task routing
├── pipelines/                     # Layer 2 — numbered stage files
│   ├── 01-research.md
│   ├── 02-structuring.md
│   ├── 03-code-generation.md
│   ├── 04-documentation.md
│   └── 05-proof-of-concept.md
├── prompts/                       # End-to-end workflow entrypoints
│   ├── new-dotnet-api.md
│   ├── update-dotnet-api.md
│   ├── content-pipeline.md
│   ├── business-process-modernization.md
│   └── clean-code-review.md
├── references/                    # Layer 3 — stable reference material (factory)
│   ├── conventions.md             # Coding standards
│   ├── glossary.md                # Domain terms
│   ├── voice.md                   # Communication style
│   ├── rate-limiting.md           # Large operation handling
│   └── refactoring.md             # Code improvement patterns
├── .universal-mwp/                # MWP state management (product)
│   ├── protocol/                  # Protocol definitions
│   │   └── tick-contract.md       # Canonical execution rules
│   ├── context/                   # Session state
│   │   ├── active-context.md
│   │   ├── progress.md
│   │   ├── tech-context.md
│   │   └── product-context.md
│   ├── queue/                     # Task queue and approvals
│   │   ├── inbox.md
│   │   └── approvals.md
│   ├── icm/                       # Preference learning
│   │   ├── preference-signals.json
│   │   ├── preference-rules.yaml
│   │   └── decision-log.md
│   ├── policy/
│   │   └── local-tick.yaml        # Risk classification config
│   ├── REQUIREMENTS.md            # What to build
│   └── STANDARDS.json             # Code style guidelines
├── .kiro/                         # Kiro configuration
│   └── steering/
│       └── mwp-protocol.md        # Kiro entry point (pointer)
└── [your existing project folders]
```

---

## Layer Reference

| Layer | File/Folder | Question | Token Budget |
|-------|-------------|----------|--------------|
| 0 | `IDENTITY.md` | "Where am I?" | ~500 tokens |
| 1 | `CONTEXT.md` | "Where do I go?" | ~300 tokens |
| 2 | `prompts/`, `pipelines/` | "What workflow and stage do I run?" | 300-600 tokens per stage |
| 3 | `references/`, `.universal-mwp/icm/` | "What rules apply?" | 500-2K tokens |
| 4 | `.universal-mwp/context/` | "What am I working with?" | varies |

---

## Reading Order

1. **IDENTITY.md** (this file) — workspace map
2. **CONTEXT.md** — task routing
3. **`.universal-mwp/protocol/tick-contract.md`** — execution rules
4. **Workflow prompt, then its stage file(s)** — for current task
5. **Context files** — only what the stage needs

---

## Rules

1. **Outputs go to** `.universal-mwp/OUTPUT/`
2. **Preference rules** in `.universal-mwp/icm/preference-rules.yaml` are human-editable
3. **Stage gates** use `STAGE_COMPLETE.md` files — check these before resuming
4. **Context loads lazily** — read only what the current stage needs
5. **One home per fact** — no duplicate definitions

---

## Related Resources

- MWP Protocol: `.universal-mwp/protocol/tick-contract.md`
- ICM Research: https://github.com/RinDig/Model-Workspace-Protocol-MWP-
- Kiro Documentation: Use `/guide` command in Kiro CLI

# Glossary

Domain-specific terms and definitions.

---

## MWP Terms

| Term | Definition |
|------|------------|
| **RoundTuit** | Repetitive Operational Unit for Nested Development: Text-Unit Iterative Tracker — the project name for this workflow engine |
| **Tick** | Single execution cycle — process one task from inbox |
| **Manifest** | The `.universal-mwp/` folder containing all MWP state |
| **Stage Gate** | `STAGE_COMPLETE.md` file marking a stage as done |
| **ICM** | Interpretable Context Methodology — preference learning system |
| **Preference Signal** | Observed user decision (approved/denied) |
| **Preference Rule** | Derived auto-approval rule with confidence score |

---

## Architecture Terms

| Term | Definition |
|------|------------|
| **CQRS** | Command Query Responsibility Segregation |
| **OpResult** | Operation result pattern — success/error without exceptions |
| **Decorator Chain** | Stack of cross-cutting concerns (logging, validation, etc.) |
| **CompositionRoot** | Where all DI registrations happen |

---

## Domain Terms

<!-- Add your domain-specific terms here -->

| Term | Definition |
|------|------------|
| | |

---

## Related Architectures

### 4-File System (SOUL, MEMORY, USER, AGENTS)

Some AI agent frameworks use a "4-file architecture" with similar principles to ICM's layered context. The concepts overlap but use different naming and structure:

| 4-File Concept | Purpose | ICM Equivalent |
|----------------|---------|----------------|
| **SOUL** | Core identity/purpose | `IDENTITY.md` + workflow prompts |
| **MEMORY** | Persistent knowledge | `.universal-mwp/context/` + `icm/` |
| **USER** | User preferences/context | `.universal-mwp/context/product-context.md` + preference learning |
| **AGENTS** | Available tools/agents | `prompts/` + `pipelines/` (workflow definitions) |

**Key difference**: The 4-file system consolidates each concern into a single file. ICM distributes the same concerns across a folder hierarchy with layered loading — entry files route, stage files define work, the filesystem is the state machine.

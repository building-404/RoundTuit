# Tool Compatibility Reference

## Prompt/Context Directories

Where to deploy this engine's files for each AI tool:

| Tool | Prompt Directory | Reference Syntax |
|---|---|---|
| Amazon Q | `~/.aws/amazonq/prompts/` | `@prompt-name` |
| GitHub Copilot | `.github/copilot-instructions.md` (project) | N/A |
| Cursor | `.cursor/rules/` (project) | `@file` |
| Kiro | `.kiro/` (project) | Specs/hooks |
| Claude Code | `CLAUDE.md` (project root) | N/A |

## Project-Level Standards Locations

Where to find coding standards and architecture docs in target projects:

| Tool | Standards Path |
|---|---|
| Amazon Q | `.amazonq/rules/*.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/*.md` |
| Claude Code | `CLAUDE.md` |
| Generic | Project root docs (`STANDARDS.md`, `CONTRIBUTING.md`) |

## Notes

- When loading standards from a target project, check all known locations above
- This table should be updated as new AI tooling emerges
- The engine itself remains tool-agnostic — this reference exists only for deployment and discovery

# Tech Context

Durable technical facts about this workspace. Read at the start of a task so
the agent doesn't re-discover the same details every tick.

## Stack

- **Language / runtime**: {e.g. .NET 8, Node 20, Python 3.12}
- **Build**: {e.g. dotnet build, npm run build}
- **Test**: {e.g. dotnet test, npm test}
- **Lint / format**: {e.g. dotnet format, eslint, prettier}

## Repositories / projects

- {repo or project} — {one-line purpose}

## Key patterns / standing instructions

- Use the `gh` CLI (or a GitHub MCP server) for all GitHub research — never
  web-fetch or raw.githubusercontent.com URLs.
- Let secrets load transparently via the config provider / user-secrets.
  Never patch tracked config with secret values; never echo them.
- {project-specific patterns}

## Environments

- {dev / QA / prod details, connection notes — NO secret values}
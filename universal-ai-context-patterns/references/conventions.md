# Conventions

Coding standards and patterns for this project.

---

## .NET Conventions

> If this is a .NET project, reference the full conventions from the MWP engine.
> See: `conventions/dotnet.md`

### Quick Reference

- **OpResult<T>** everywhere, never throw for control flow
- **Routes** auto-generated from message names
- **Primary constructors** for DI
- **Record types** for messages
- **Functional composition** (Map, Bind, Match) preferred
- **No .Result** on async operations

---

## Naming Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{Verb}{Noun}Command` | `CreateUserCommand` |
| Query | `Get{Noun}Query` | `GetUserQuery` |
| Handler | `{Command/Query}Handler` | `CreateUserCommandHandler` |
| DataAccess interface | `IManage{Entity}Data` | `IManageUserData` |
| DataAccess impl | `{Entity}DataAccess` | `UserDataAccess` |

---

## Test Naming

Pattern: `{Method}_{Scenario}_{Expected}`

```
CreateUser_WithValidData_ReturnsSuccess
CreateUser_WithMissingEmail_ReturnsValidationError
```

---

## SOLID Principles

- **Single Responsibility:** One handler per message, one decorator per concern
- **Open/Closed:** New behavior via decorators, never modify existing handlers
- **Liskov Substitution:** All implementations interchangeable behind interfaces
- **Interface Segregation:** Focused interfaces per entity
- **Dependency Inversion:** Constructor-inject abstractions only

---

## Project-Specific Rules

<!-- Add your project-specific conventions here -->

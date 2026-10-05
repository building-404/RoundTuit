# Refactoring Guidelines

Patterns for cleaning up and improving code structure.

---

## Core Engineering Principles

- **Composition over inheritance** — Use interfaces, delegates, and object composition. Avoid deep hierarchies.
- **Separation of concerns** — Keep domain, data models, infrastructure, and presentation layers distinct.
- **Immutability first** — Prefer records and read-only types. Mutate state explicitly in encapsulated scopes.
- **Pragmatic patterns** — Use functions, pattern matching, and closures. Avoid boilerplate from legacy OOP patterns.
- **KISS & YAGNI** — No premature abstractions. Add complexity only when explicitly needed.

---

## Refactoring Patterns

### 1. Replace Class Boilerplate with Functions

- Single-method interfaces → function delegates or lambdas
- Template methods → function composition

### 2. Simplify Dispatch with Pattern Matching

- Visitor patterns and type-checking cascades → algebraic data types + pattern matching

### 3. Eliminate Mutable State Containers

- Stateful data classes → immutable records
- Manual builders → `with` expressions or copy constructors

### 4. Clean Up As You Go

- Small, single-responsibility functions
- Remove dead code and redundant abstractions

---

## Code Generation Requirements

- **Type safety** — Strict typing, pattern matching, null-safety
- **Pure/impure separation** — Isolate side effects (I/O, logging, mutation)
- **Explicit dependencies** — Primary constructors or parameter injection. No hidden globals.
- **Modern idioms** — Primary constructors, records, expression-bodied members, top-level functions

---

## Output Protocol

1. **Provide code directly** — no filler or fluff
2. **Summarize key design decisions** — after the code, in bullet form
3. **Preserve existing behavior** — unless explicitly asked to change

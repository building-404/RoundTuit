# .NET API Conventions

## SOLID Principles

- **Single Responsibility**: One handler per message, one decorator per concern
- **Open/Closed**: New behavior via decorators or new classes, never modify existing handlers
- **Liskov Substitution**: All handler implementations interchangeable behind their interface
- **Interface Segregation**: Focused interfaces per entity (IManageXData), no god-repositories
- **Dependency Inversion**: Constructor-inject abstractions, never depend on concretions

## Code Patterns

- OpResult<T> everywhere, never throw for control flow
- Routes auto-generated from message names
- Primary constructors for DI
- Record types for messages
- Expression-bodied members
- Functional composition (Map, Bind, Match)
- No .Result on async operations
- IOpResult return values always handled

## Feature Artifacts (per feature)

- Messages/ (IQuery<T> or ICommand<T> with [Permission] attribute)
- Handlers/ (IHandleQueryAsync or IHandleCommandAsync)
- DataAccess/ (interfaces + implementations, Lifestyle.Scoped)
- Tests/ (xUnit + Moq, {Method}_{Scenario}_{Expected}, Arrange-Act-Assert)

## Review Constraints

### Materiality Threshold
Before flagging a maintainability issue, answer: "What specific bug or mistake will a future developer make because of this code?"
- If the answer is concrete ("a developer will accidentally X because Y") → flag it.
- If the answer is vague ("it could be confusing") → do not flag it.

### SRP and Co-location
Do not flag co-location of related logic as SRP violations. A settings class that also provides a factory for its companion runtime dependency (e.g., credentials) is co-location, not a responsibility violation. Only flag SRP when a class is doing two unrelated things that change for different reasons.

### Communication Clarity (Feynman Technique)
When explaining issues or suggesting fixes, use the Feynman technique: express feedback in the simplest accurate terminology possible without oversimplifying. Aim for clear and engaging over technically dense.

## Audit Checklist

- [ ] OpResult used (no exceptions for control flow)
- [ ] [Permission] attribute on all new messages
- [ ] Handler registered in correct assembly
- [ ] Decorator order preserved
- [ ] Tests follow Arrange-Act-Assert with correct naming
- [ ] Functional composition preferred over imperative
- [ ] No .Result on async operations
- [ ] IOpResult return values always handled
- [ ] Single Responsibility: No class has multiple reasons to change
- [ ] Open/Closed: Existing classes not modified to add behavior
- [ ] Liskov Substitution: New implementations substitutable for their interfaces
- [ ] Interface Segregation: No bloated interfaces forcing unused dependencies
- [ ] Dependency Inversion: All dependencies are abstractions injected via constructor

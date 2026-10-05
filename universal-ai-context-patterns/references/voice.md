# Voice

Tone, audience, and communication standards.

---

## Communication Style

- **Be concise** — skip filler phrases
- **Show, don't tell** — prefer examples over explanations
- **Be direct** — lead with the answer, then explain if needed
- **Match the user** — formal for formal, casual for casual

---

## Code Comments

- Include comments only for **non-obvious logic**
- Explain **why**, not what
- Reference issue/task numbers for complex decisions

```csharp
// Good: Explains why
// Using explicit lock instead of SemaphoreSlim because we need 
// reentrant behavior for nested calls (see DEV-1234)
private readonly object _lock = new();

// Bad: Explains what
// Locks the object
private readonly object _lock = new();
```

---

## Error Messages

User-facing messages should:
- State what happened
- Suggest how to fix it
- Avoid technical jargon

---

## Documentation

- Lead with the **most important information**
- Use **active voice**
- Include **code examples** for API documentation
- Cite sources for factual claims

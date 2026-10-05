# Clean Code Review

## Pre-Review

1. **Identify target**: Resolve what's being reviewed — file path, PR URL, commit SHA, or combination.
2. **Check archive**: Read `{{MANIFEST_PATH}}/reviews/` for an existing entry matching the same target (PR number, commit SHA, or file+content hash). If found, surface prior findings and ask if a re-review is wanted. If not, stop.
3. **Write state**: Create `{{CONTEXT_PATH}}/review/in-progress.md` with the target identifier and timestamp.

On resume: if `in-progress.md` exists without a corresponding archive entry, continue the review from where context allows.

---

## Review

Act as a senior software craftsman and expert in Clean Code. Review this code specifically for adherance to Clean Code principles.

1. Functions: Are they small? Do they do only one thing (Single Responsibility Principle)? Is the level of abstraction consistent?
2. Naming: Are variables and functions named in a way that reveals intent? (Self-Documenting Code)
3. Comments: Does the code rely on comments rather than clarity? Recommend removing comments that explain what the code does rather than why.
4. Complexity: Identify code smells, excessive nesting, and high cyclomatic complexity.
5. Boy Scout Rule: Suggest small refactorings to leave this code cleaner than you found it.

Focus on readability and maintainability over cleverness.

### Review Constraints

#### Materiality Threshold
Before flagging a maintainability issue, answer: "What specific bug or mistake will a future developer make because of this code?"
- If the answer is concrete ("a developer will accidentally X because Y") → flag it.
- If the answer is vague ("it could be confusing") → do not flag it.

#### SRP and Co-location
Do not flag co-location of related logic as Single Responsibility Principle violations. A settings class that also provides a factory for its companion runtime dependency (e.g., credentials) is co-location, not a responsibility violation. Only flag SRP when a class is doing two unrelated things that change for different reasons.

#### Communication Clarity (Feynman Technique)
When explaining issues or suggesting fixes, use the Feynman technique: express feedback in the simplest accurate terminology possible without oversimplifying. Aim for clear and engaging over technically dense.

---

## Post-Review

1. **Archive**: Write `{{MANIFEST_PATH}}/reviews/{RUN_TIMESTAMP}-{identifier}.md` with:
   ```markdown
   # Review: {target}
   Date: {timestamp}
   Target: {PR URL, commit SHA, or file path}
   Outcome: {approved | changes-requested}
   ## Findings
   {summary of issues found, or "No material issues"}
   ```
2. **Clean up state**: Remove `in-progress.md`.

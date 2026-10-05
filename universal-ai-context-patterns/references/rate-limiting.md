# Rate Limiting Best Practices

Guidelines for handling large operations efficiently.

---

## For Large Operations

When performing codebase analysis, multi-file refactoring, or documentation generation:

1. **Break tasks into smaller chunks** — Process files in batches or directory by directory
2. **Use `consolidate=false` for large codebases** — Generate individual docs first, then consolidate
3. **Progress updates** — Provide status after each major step of long operations
4. **Suggest targeted focus** — Recommend analyzing specific directories if performance lags
5. **Default to concise output** — Trim verbose explanations when the task is straightforward
6. **Batch related operations** — Group file reads/writes to minimize round trips
7. **Preserve manual content** — When regenerating docs, identify and preserve user-customized sections (look for HTML comments like `<!-- Custom Instructions -->`)

---

## Large Task Protocol

For large codebase operations:

1. **Start with overview** — Use `generate_codebase_overview` first for high-level structure
2. **Request user confirmation** — Before heavy operations, ask: "Proceed with [specific task]?"
3. **Progress markers** — Output `✅ Step X complete` after major phases
4. **Split into steps** — For complex tasks, ask: "Split into smaller steps?"
5. **Fallback to `consolidate=false`** — For large codebases, default to individual doc generation

# Update Existing .NET API

**Use When**: Adding features or modifying an existing API built from the template  
**Output**: New/modified files ready to merge into existing solution

```
We are executing the universal MWP framework for .NET API modification.

MANIFEST_PATH = <workspace-root>/.universal-mwp/
TASK_ID = {{TASK_ID}}
RUN_TIMESTAMP = {{RUN_TIMESTAMP}}
EXISTING_CODE_PATH = {{EXISTING_CODE_PATH}}
EXECUTION_MODE = update
CHANGE_TYPE = {{CHANGE_TYPE}} (allowed: query|command|decorator|dataaccess|feature)
CONTEXT_PATH = {{MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}

Treat all instructions as abstract laws. Fill blanks from manifest.
Load conventions/dotnet.md as the coding standard for all generated code.

SETUP:
1. Resolve {{MANIFEST_PATH}} from workspace root
2. Check {{CONTEXT_PATH}}/ for existing STAGE_COMPLETE.md files — resume from last incomplete stage
3. Create {{CONTEXT_PATH}}/ with subdirectories: research/, script-lab/, code-gen/
4. Create OUTPUT/

STAGE 1: RESEARCH
loads: [REQUIREMENTS.md, tech-context.md]
1. Analyze existing code at {{EXISTING_CODE_PATH}}
2. Load architecture docs and coding standards from {{EXISTING_CODE_PATH}} (see conventions/tool-compatibility.md for common locations)
3. Load {{MANIFEST_PATH}}/REQUIREMENTS.md (what to add/change)
4. Execute research phases:
   - Inventory: Current messages, handlers, decorators, registrations
   - Thematic Extraction: Existing patterns and conventions in use
   - Gap Analysis: What's needed vs what exists
   - Synthesis: Minimal change set required
   - Brief: Impact assessment and risks
5. Save to {{CONTEXT_PATH}}/research/
6. Write {{CONTEXT_PATH}}/research/STAGE_COMPLETE.md

STAGE 2: STRUCTURING
loads: [STANDARDS.json, product-context.md, {{CONTEXT_PATH}}/research/]
1. Load {{MANIFEST_PATH}}/STANDARDS.json
2. Map changes to existing architecture:
   - Which files are new?
   - Which files need modification?
   - What registrations must be added?
3. Verify no decorator ordering conflicts
4. Save to {{CONTEXT_PATH}}/script-lab/
5. Write {{CONTEXT_PATH}}/script-lab/STAGE_COMPLETE.md

STAGE 3: CODE GENERATION
loads: [STANDARDS.json, tech-context.md, {{CONTEXT_PATH}}/script-lab/]
1. Generate ONLY new/modified files
2. Match existing code style exactly (primary constructors, records, OpResult)
3. Apply SOLID principles (see conventions/dotnet.md → SOLID Principles)
4. Add tests for new functionality
5. Update CompositionRoot registrations (augment, don't replace)
6. Update Permissions.cs if new permissions needed
7. Audit against conventions/dotnet.md → Audit Checklist
8. Save to {{MANIFEST_PATH}}/OUTPUT/
9. Write {{CONTEXT_PATH}}/code-gen/STAGE_COMPLETE.md

DELIVERABLES:
- New/modified files in OUTPUT/
- CHANGES.md with file-by-file diff summary
- integration-checklist.md for manual verification

Execute all stages now. Skip any stage with an existing STAGE_COMPLETE.md.
```

## Post-Execution

Follow `conventions/post-execution.md`

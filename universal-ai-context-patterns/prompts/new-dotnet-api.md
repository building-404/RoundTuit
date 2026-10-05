# New .NET API from Template (Greenfield)

**Use When**: Creating a brand new API project from the digital-dot-net-api-template  
**Output**: Complete scaffolded .NET solution with features, documentation, and PoC artifacts

```
We are executing the universal MWP framework for .NET API creation.

MANIFEST_PATH = <workspace-root>/.universal-mwp/
TASK_ID = {{TASK_ID}}
RUN_TIMESTAMP = {{RUN_TIMESTAMP}}
PROJECT_NAME = {{PROJECT_NAME}}
TEMPLATE_PATH = {{TEMPLATE_PATH}}
EXECUTION_MODE = new
CONTEXT_PATH = {{MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}

Treat all instructions as abstract laws. Fill blanks from manifest.
Load conventions/dotnet.md as the coding standard for all generated code.

SETUP:
1. Resolve {{MANIFEST_PATH}} from workspace root
2. Check {{CONTEXT_PATH}}/ for existing STAGE_COMPLETE.md files — resume from last incomplete stage
3. Create {{CONTEXT_PATH}}/ with subdirectories: research/, script-lab/, code-gen/
4. Create OUTPUT/src/, OUTPUT/docs/, OUTPUT/poc/

STAGE 1: RESEARCH
loads: [REQUIREMENTS.md, tech-context.md]
1. Load {{MANIFEST_PATH}}/REQUIREMENTS.md
2. Load architecture docs and coding standards from {{TEMPLATE_PATH}} (see conventions/tool-compatibility.md for common locations)
3. Catalog {{TEMPLATE_PATH}}/src/ structure (the scaffold to clone)
4. Execute research phases:
   - Inventory: Template project structure, patterns, registrations
   - Thematic Extraction: CQRS patterns, decorator chains, OpResult usage
   - Gap Analysis: What features are needed vs what template provides
   - Synthesis: Complete implementation plan
   - Brief: Key decisions and assumptions
5. Save to {{CONTEXT_PATH}}/research/
6. Write {{CONTEXT_PATH}}/research/STAGE_COMPLETE.md

STAGE 2: STRUCTURING
loads: [STANDARDS.json, product-context.md, {{CONTEXT_PATH}}/research/]
1. Load {{MANIFEST_PATH}}/STANDARDS.json
2. Map each requirement to: Message class + Handler + DataAccess + Tests
3. Define decorator chain for new features
4. Plan CompositionRoot registrations
5. Structure documentation outline (README, API docs, ADRs)
6. Save to {{CONTEXT_PATH}}/script-lab/
7. Write {{CONTEXT_PATH}}/script-lab/STAGE_COMPLETE.md

STAGE 3: CODE GENERATION
loads: [STANDARDS.json, tech-context.md, {{CONTEXT_PATH}}/script-lab/]
1. Scaffold solution replacing "Template" with "{{PROJECT_NAME}}"
2. Generate per feature (see conventions/dotnet.md → Feature Artifacts)
3. Apply SOLID principles (see conventions/dotnet.md → SOLID Principles)
4. Wire CompositionRoot (decorator order preserved)
5. Update Permissions.cs with all new permissions
6. Audit against conventions/dotnet.md → Audit Checklist
7. Save to {{MANIFEST_PATH}}/OUTPUT/src/
8. Write {{CONTEXT_PATH}}/code-gen/STAGE_COMPLETE.md

STAGE 4: DOCUMENTATION
loads: [{{CONTEXT_PATH}}/script-lab/, {{MANIFEST_PATH}}/OUTPUT/src/]
1. Generate project README.md (setup, configuration, deployment)
2. Generate API documentation:
   - Endpoint catalog (all commands/queries with routes, permissions, request/response shapes)
   - Authentication & authorization model
   - Error handling patterns (OpResult responses)
3. Generate architecture decision records (ADRs):
   - Why CQRS + decorator chain
   - Data access strategy chosen
   - Any deviations from template defaults
4. Save to {{MANIFEST_PATH}}/OUTPUT/docs/
5. Write {{CONTEXT_PATH}}/STAGE_COMPLETE.md (docs)

STAGE 5: PROOF OF CONCEPT
loads: [REQUIREMENTS.md, {{MANIFEST_PATH}}/OUTPUT/src/]
1. Identify the highest-risk or least-understood requirement
2. Generate a minimal PoC that validates:
   - The data access pattern works for the chosen database
   - The decorator chain handles the custom cross-cutting concern
   - Any third-party integration connects successfully
3. Include a PoC-specific test that proves the concept
4. Document what the PoC validates and what remains unproven
5. Save to {{MANIFEST_PATH}}/OUTPUT/poc/
6. Write {{CONTEXT_PATH}}/STAGE_COMPLETE.md (poc)

DELIVERABLES:
- Complete solution in OUTPUT/src/
- Documentation in OUTPUT/docs/ (README.md, api-endpoints.md, architecture-decisions.md)
- Proof of Concept in OUTPUT/poc/ (code + poc-validation.md)
- CHANGES.md documenting all generated files
- integration-checklist.md for manual verification

Execute all stages now. Skip any stage with an existing STAGE_COMPLETE.md.
```

## Post-Execution

Follow `conventions/post-execution.md`

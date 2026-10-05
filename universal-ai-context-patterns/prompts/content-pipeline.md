# Content Pipeline

**Use When**: Research, content creation, iteration, or project migration  
**Output**: Research docs, branded content, or refined deliverables

```
We are executing the universal MWP framework content pipeline.

MANIFEST_PATH = {{MANIFEST_PATH}}
TASK_ID = {{TASK_ID}}
RUN_TIMESTAMP = {{RUN_TIMESTAMP}}
MODE = {{full|research|content|iterate|migrate}}
CONTEXT_PATH = {{MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}

Treat all instructions as abstract laws. Fill blanks from manifest.

SETUP:
1. Resolve {{MANIFEST_PATH}} from workspace root
2. Check {{CONTEXT_PATH}}/ for existing STAGE_COMPLETE.md files — resume from last incomplete stage

--- MODE: full (Research → Content) ---

STAGE 1: RESEARCH
loads: [TOPICS.md, SOURCE_MATERIAL/, tech-context.md]
1. Load {{MANIFEST_PATH}}/TOPICS.md (research objectives)
2. Catalog {{MANIFEST_PATH}}/SOURCE_MATERIAL/
3. Execute research phases: Inventory → Thematic Extraction → Gap Analysis → Synthesis → Context Brief
4. Save to {{CONTEXT_PATH}}/research/
5. Write {{CONTEXT_PATH}}/research/STAGE_COMPLETE.md

STAGE 2: CONTENT STRUCTURING
loads: [BRANDS.json, {{CONTEXT_PATH}}/research/, product-context.md]
1. Load {{MANIFEST_PATH}}/BRANDS.json (brand voice)
2. Use Stage 1 outputs as research input
3. Execute content phases: Format Definition → Content Mapping → Draft Assembly → Brand Audit → Polish
4. Save working to {{CONTEXT_PATH}}/script-lab/
5. Save final to {{MANIFEST_PATH}}/OUTPUT/final-deliverable.md
6. Write {{CONTEXT_PATH}}/script-lab/STAGE_COMPLETE.md

--- MODE: research (Stage 1 only) ---

loads: [TOPICS.md, SOURCE_MATERIAL/, tech-context.md]
1. Load {{MANIFEST_PATH}}/TOPICS.md
2. Catalog {{MANIFEST_PATH}}/SOURCE_MATERIAL/
3. Execute research phases: Inventory → Thematic Extraction → Gap Analysis → Synthesis → Context Brief
4. Save to {{CONTEXT_PATH}}/research/
5. Write {{CONTEXT_PATH}}/research/STAGE_COMPLETE.md

--- MODE: content (Stage 2 only, research already exists) ---

RESEARCH_INPUT_PATH = {{RESEARCH_INPUT_PATH}}
OUTPUT_FORMAT = {{OUTPUT_FORMAT}}

loads: [BRANDS.json, {{RESEARCH_INPUT_PATH}}/, product-context.md]
1. Load {{MANIFEST_PATH}}/BRANDS.json
2. Load research from {{RESEARCH_INPUT_PATH}}/
3. Execute content phases: Format Definition → Content Mapping → Draft Assembly → Brand Audit → Polish
4. Save working to {{CONTEXT_PATH}}/script-lab/
5. Save final to {{MANIFEST_PATH}}/OUTPUT/final-deliverable.md
6. Write {{CONTEXT_PATH}}/script-lab/STAGE_COMPLETE.md

--- MODE: iterate (Refine existing output) ---

ITERATION_FOCUS = {{tone|structure|audience|length|clarity}}
REFINEMENT_NOTES = {{REFINEMENT_NOTES}}

loads: [BRANDS.json, OUTPUT/final-deliverable.md]
1. Load {{MANIFEST_PATH}}/OUTPUT/final-deliverable.md
2. Load {{MANIFEST_PATH}}/BRANDS.json
3. Analyze against brand standards, focus on {{ITERATION_FOCUS}}
4. Apply {{REFINEMENT_NOTES}}
5. Save to {{MANIFEST_PATH}}/OUTPUT/final-deliverable-v2.md
6. Create iteration report to {{CONTEXT_PATH}}/script-lab/

--- MODE: migrate (Swap to new project manifest) ---

NEW_PROJECT_MANIFEST = {{NEW_PROJECT_MANIFEST}}
EXECUTION_MODE = {{full|research|content}}

1. Load new manifest: {{NEW_PROJECT_MANIFEST}}
2. Verify BRANDS.json, TOPICS.md, SOURCE_MATERIAL/ exist
3. Execute {{EXECUTION_MODE}} using new manifest

---

Execute the specified MODE now. Skip any stage with an existing STAGE_COMPLETE.md.
```

## Post-Execution

Follow `conventions/post-execution.md`

# Business Process Modernization

**Use When**: Reworking an existing business process or its supporting systems to take advantage of modern technologies

**Output**: An approved behavior brief, frozen acceptance tests, a modern implementation, and a verification and adoption report

This workflow uses four distinct AI roles across two workspaces. Each role runs in a separate chat session and performs only its assigned stage. A human operator controls exact artifact transfers.

| AI role | Function | Workspace |
|----------|----------|-----------|
| Role 1 | Process Analyst | Discovery |
| Role 2 | Transfer Reviewer | Discovery |
| Role 3 | Test Architect | Modernization |
| Role 4 | Modernization Developer | Modernization |

The discovery-side developer and modernization-side developer are human checkers, not AI roles. They must be two different people; neither is Role 1, 2, 3, or 4.

## Workspace Boundary

```text
DISCOVERY_ROOT = <workspace containing the existing process, systems, and source material>
MODERNIZATION_ROOT = <separate workspace for tests and the new implementation>
DISCOVERY_MANIFEST_PATH = {{DISCOVERY_ROOT}}/.universal-mwp/
MODERNIZATION_MANIFEST_PATH = {{MODERNIZATION_ROOT}}/.universal-mwp/
TASK_ID = {{TASK_ID}}
RUN_TIMESTAMP = {{RUN_TIMESTAMP}}
```

## Workspace Setup and Resume

- Initialize `{{DISCOVERY_MANIFEST_PATH}}` and `{{MODERNIZATION_MANIFEST_PATH}}` independently. Never copy one workspace's manifest into the other.
- Each agent reads and updates only the manifest in its own workspace. No agent needs access to the other workspace's manifest to resume.
- Use these stage gates:

| Stage | Workspace | Completion gate |
|-------|-----------|-----------------|
| 1: Current-State Analysis | Discovery | `{{DISCOVERY_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/analysis/STAGE_COMPLETE.md` |
| 2: Handoff Review | Discovery | `{{DISCOVERY_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/handoff/STAGE_COMPLETE.md` |
| 3: Acceptance-Test Design | Modernization | `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/acceptance-tests/STAGE_COMPLETE.md` |
| 4: Modernization Implementation | Modernization | `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/implementation/STAGE_COMPLETE.md` |
| 5: Verification and Adoption | Modernization | `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/verification/STAGE_COMPLETE.md` |

- On resume, inspect local stage gates in order and verify that each gate's required outputs exist. If a gate exists but an output is missing or inconsistent, stop and report the stage incomplete.
- Stage 3 cannot start until the modernization workspace has the approved intake package and a successful receipt entry in its local `transfer-log.md`.
- Stage 4 outputs remain in `OUTPUT/`; its completion gate is execution state under `context/.../implementation/`.

## Human Accountability

- Assign a discovery-side developer and a modernization-side developer as two different people. The discovery-side developer may inspect the existing system and validate the behavior brief but does not implement the modernization. The modernization-side developer must not access the source system, discovery workspace, or discovery chat history.
- Before transfer, the discovery-side developer confirms the outgoing package contains only the approved files. After transfer, the modernization-side developer performs the receipt gate before Role 3 reads any brief content into AI context. Record release and receipt checks in the respective workspace's `transfer-log.md`.
- The human operator transfers the exact approved files and does not add undocumented implementation guidance. The process owner approves business outcomes and any material changes to requirements. These responsibilities may be assigned according to the organization's controls, but the two developer roles must remain separate people.
- Tool selection is platform-neutral. Use only chat services and accounts approved for the material they receive, and verify the required workspace access controls independently of prompt instructions.
- Approval/release/receipt entries are recorded attestations for audit. They do not cryptographically authenticate identity or prevent tampering. Apply stronger organization-required signing controls separately.

- Roles 1 and 2 run only in the discovery workspace. Roles 3 and 4 run only in the modernization workspace.
- Enforce this boundary with separate machines or accounts and access permissions. Separate folders on a machine that can access both workspaces are not an access boundary.
- Do not share source repositories, repository history, discovery notes, chat transcripts, synced storage, or clipboard history with the modernization workspace.
- Before any proprietary material is submitted to a chat service, confirm that the service and account are approved for that material.
- A human may transfer only the approved handoff package. Do not add unrecorded verbal or written implementation details. If clarification is needed, route the question to Role 1, have Role 2 review the revised answer, and transfer the updated package with a new handoff record.
- If these access controls cannot be enforced, stop this workflow and agree on a less isolated modernization process before proceeding.

Each workspace keeps its own `.universal-mwp/` state. Never copy the discovery manifest into the modernization workspace. The only cross-workspace input is the human-approved handoff package and its transfer record.

## Clarification and Revision Rules

- Stop the current stage when a blocking ambiguity could change a business rule, input, expected outcome, control, or scope. Do not fill the gap with an assumption.
- Route the question to the Process Analyst and the discovery-side developer. The Transfer Reviewer screens the answer; the process owner approves any material behavior change. Record each response as a versioned clarification linked to the brief and affected requirement IDs.
- Editorial corrections that do not change behavior may be recorded without invalidating unaffected tests. Any material change invalidates affected tests and their prior approval; update, review, and freeze a new suite version before implementation resumes.
- If the same blocking issue remains unresolved after two clarification exchanges, pause and escalate to the process owner. Do not continue by accumulating assumptions.
- An implementation defect returns to Stage 4 with the approved test suite unchanged. If a test defect is confirmed, document the reason, obtain human approval, revise the affected tests, repeat coverage review, and freeze a new suite version before resuming implementation.

## Stage 1: Current-State Analysis

**Role 1: Process Analyst**

**Workspace**: Discovery

Review authorized source material and document observed business behavior, not a proposed implementation.

1. Inventory process actors, triggers, inputs, outputs, decisions, business rules, exceptions, controls, integrations, service levels, and known pain points.
2. Separate confirmed behavior from assumptions and open questions. Assign stable requirement IDs to confirmed behaviors.
3. Use business terminology. Do not copy source code, comments, proprietary identifiers, or implementation-specific structure into the draft brief.
4. Record modernization goals, constraints, data sensitivity, and out-of-scope behavior. With the process owner, capture baseline measures and target outcomes where available; label qualitative goals explicitly and record the measure, data source, owner, and evaluation time when known.
5. Include a `Technical Assumptions` section in `modernization-brief-draft.md`. List only reviewed assumptions needed to evaluate the proposed modernization, with validation method and risk if unvalidated. If none are identified, state `None identified`. Do not include source code, internal schemas, or source-derived implementation structure.
6. Save working analysis and `modernization-brief-draft.md` under `{{DISCOVERY_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/analysis/`.
7. Write the Stage 1 completion gate only when the draft covers normal flows, edge cases, unresolved questions, and the Technical Assumptions section.

## Stage 2: Handoff Review

**Role 2: Transfer Reviewer**

**Workspace**: Discovery

Review the draft independently before anything is transferred.

1. Check each requirement for observable inputs, expected outcomes, relevant exceptions, and a clear source of confirmation.
2. Reject source excerpts, code-like blocks, proprietary identifiers, copied implementation structure, unsupported assumptions, and examples containing real sensitive data.
3. Confirm that the brief describes required business outcomes without prescribing a source-derived architecture.
4. Return rejected material to Role 1 for revision. Do not edit source material or author implementation details.
5. Verify that the Technical Assumptions section is present, contains reviewed assumptions or `None identified`, and does not disclose source-derived implementation details.
6. On approval, write `approved-modernization-brief.md` and `handoff-record.md` under `{{DISCOVERY_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/handoff/`. The record includes the brief version, requirement IDs, reviewer, approver, timestamp, approval statement, exact permitted-file list, exclusions, and SHA-256 values for the brief and optional synthetic examples.
7. The discovery-side developer verifies the file allowlist and recorded hashes, then adds a release attestation with identity and timestamp to the handoff record and logs the checks in the discovery manifest's `transfer-log.md`.
8. Write the Stage 2 completion gate only after the process owner approves the exact package and the discovery-side developer records a successful release check.

The human operator transfers only the approved brief, the optional `approved-synthetic-examples.md`, and handoff record to `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/intake/`. No other discovery artifacts cross this boundary.

## Stage 3: Acceptance-Test Design

**Role 3: Test Architect**

**Workspace**: Modernization

**Human receipt gate, before Role 3 starts**: The modernization-side developer verifies that `intake/` contains only `approved-modernization-brief.md`, optional `approved-synthetic-examples.md`, and `handoff-record.md`. Verify matching artifact versions and hashes, approval/release attestations, and release-before-receipt ordering. Use a local hash utility; it may read bytes to calculate hashes, but unapproved file contents must not be loaded into any AI context. On any failure, log the failed check in the modernization manifest's `transfer-log.md`, stop, and notify the human operator. After all checks pass, record receipt identity/time and authorize Role 3. Role 3 must not load the brief until this gate passes.

Use only the validated intake package and public platform documentation. Do not access the discovery workspace or source material. The Test Architect creates the test harness and a platform/build contract in the modernization workspace from approved platform requirements and public documentation; the human reviews these with the tests.

1. Before test design, inspect only the `Technical Assumptions` section in the approved brief. If it says `None identified`, proceed. For a listed assumption that cannot be validated through black-box tests, pause and ask the process owner to document the risk, authorize a separate feasibility investigation, or halt until it is resolved. Do not access the discovery manifest or infer unstated assumptions.
2. Create black-box tests from the requirement IDs and observable behaviors in the approved brief.
3. Cover normal flows, boundaries, exceptions, controls, and relevant non-functional requirements. Use synthetic fixtures only.
4. Create a requirement-to-test traceability matrix. Every requirement ID must map to a test or have an explicit, human-approved reason why it is not directly testable. Stop for blocking ambiguities; do not silently invent behavior.
5. Create the test harness and platform/build contract using public documentation and approved platform constraints. The test-environment contract records runtime and test-runner versions, dependency lockfiles, non-secret environment inputs, external test dependencies, and fixture/seed provenance. Save these with the tests, traceability matrix, clarification records, and contract under `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/acceptance-tests/`.
6. Run the suite against an empty or minimal baseline and record pass/fail results. Explain tests that legitimately pass without implementation; strengthen tests only when they fail to assert their requirement.
7. Build `suite-manifest.json` over every test-affecting file: tests, helpers, fixtures, harness, runner configuration, dependency lockfiles, and declared environment contract. Normalize paths to relative forward-slash paths in Unicode NFC, sort by normalized path, and record each file's category, byte length, and SHA-256 digest. Fail closed if test execution uses an undeclared file input.
8. Compute `suite_hash` as SHA-256 over the RFC 8785/JCS canonical UTF-8 serialization of exactly this payload shape, with `files` sorted by normalized path:

	 ```json
	 {
		 "files": [
			 {
				 "category": "test-file",
				 "normalized_path": "tests/feature.test.ts",
				 "sha256": "<file digest>",
				 "size_bytes": 1234
			 }
		 ],
		 "schema_version": 1,
		 "total_files": 1,
		 "total_size_bytes": 1234
	 }
	 ```

	 Exclude `generated_at`, `algorithm`, and `suite_hash` from the payload. Store the manifest in the acceptance-tests folder. Reject unsupported manifest versions or hash algorithms.
9. Have a human review the traceability matrix, baseline results, harness, platform/build contract, test-environment contract, and manifest. Freeze the reviewed suite before implementation and record its version and hash in the Stage 3 completion gate.

## Stage 4: Modernization Implementation

**Role 4: Modernization Developer**

**Workspace**: Modernization

Use only the frozen acceptance-test suite, test harness, approved platform constraints, and build instructions. Do not access the approved brief, discovery workspace, or source material.

1. Implement the smallest maintainable design that satisfies the frozen tests, platform/build contract, and approved platform constraints. Do not infer requirements from unavailable source material.
2. Do not change acceptance tests. If a test or requirement is ambiguous, stop and submit a clarification request through the versioned process above.
3. Run the available test suite after each meaningful change and record results.
4. Save implementation under `{{MODERNIZATION_MANIFEST_PATH}}/OUTPUT/` and write `STAGE_COMPLETE.md` with the source revision and test results.

## Stage 5: Verification and Adoption

**Role 3: Test Architect; human acceptance required**

**Workspace**: Modernization

1. Before loading or executing the acceptance suite, use a local verifier to recompute the declared file set and suite hash. Compare it with the Stage 3 manifest and verify runtime, test-runner, dependency, and non-secret environment inputs against the test-environment contract. Any added, missing, modified, undeclared, or mismatched input fails verification; report the difference and halt before test execution. Do not load unapproved file contents into AI context during this check. Report external dependencies or nondeterministic inputs that cannot be pinned as residual risks for human acceptance.
2. Run the frozen acceptance suite against the completed implementation and verify the traceability matrix. The human confirms every requirement ID is covered or has an approved exception.
3. Report passing and failing tests, untested requirements, and remaining risks. Distinguish functional test results from business outcomes that require post-deployment measurement; do not claim those outcomes have been achieved before measurement.
4. Prepare a rollout, migration, monitoring, rollback, and user-adoption checklist appropriate to the process, including owners and timing for post-deployment outcome measures.
5. Save `verification-report.md` and `adoption-plan.md` under `{{MODERNIZATION_MANIFEST_PATH}}/OUTPUT/`.
6. The human reviews operational, security, privacy, and compliance requirements and decides whether the result is accepted for use. Write `STAGE_COMPLETE.md` to `{{MODERNIZATION_MANIFEST_PATH}}/context/{{RUN_TIMESTAMP}}-{{TASK_ID}}/verification/` with the report paths, suite-hash result, test summary, coverage exceptions, and acceptance decision.

## Completion Criteria

- The approved brief and its exact transfer are recorded.
- Acceptance tests were frozen before implementation and remain unchanged.
- All required tests pass, and uncovered behavior and residual risks are documented.
- Functional test results are reported separately from measured post-deployment business outcomes.
- A human has reviewed and accepted the implementation and adoption plan.

This workflow records its inputs, handoffs, and decisions; it does not certify legal, regulatory, or intellectual-property compliance.

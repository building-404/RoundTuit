# Convention: PR Review

A durable standard for reviewing pull requests. Two parts: (1) a mandatory
re-review checklist so a review is real (not a metadata glance), and (2) a
high-signal flag/skip bar so reviews stay noise-free.

Distilled from a long-running .NET workspace where metadata-only "reviews"
repeatedly missed real automated-reviewer findings.

---

## 1. PR re-review checklist (mandatory)

"Confirming a PR exists" is NOT reviewing it. Whenever asked to look at, review,
or revisit a PR, always pull and read ALL of these — not just PR metadata:

- [ ] PR metadata + description — `gh pr view {n} --json title,body,baseRefName,headRefName,state`
- [ ] Formal reviews — `gh api repos/{owner}/{repo}/pulls/{n}/reviews`
- [ ] Inline (line-anchored) review comments — `gh api repos/{owner}/{repo}/pulls/{n}/comments`
- [ ] Issue-level comments (incl. bot summaries) — `gh api repos/{owner}/{repo}/issues/{n}/comments`

Then:

- [ ] Treat any automated-reviewer bot output as findings to reconcile, not as
      ground truth. Verify each against the CURRENT branch head
      (`git show origin/{branch}:path`) — bot comments can be stale after later
      commits, or already addressed in a reply.
- [ ] For each open finding, state: still-open vs resolved, and the evidence
      (commit SHA, file:line, or author reply) that supports the call.
- [ ] Tooling: use `gh` / a GitHub MCP server only — never web-fetch / raw
      GitHub URLs.

Read-only PR reviews (nothing posted to GitHub, no repo change) are
`change_scope: read-only` → low risk per `policy/local-tick.yaml`. Posting a
review/comment to the live PR, or pushing to the PR branch, is a separate
action needing the usual approval (external-integration / modify-existing).

---

## 2. High-signal review bar

Goal: high-signal, minimal-noise feedback that materially impacts correctness,
safety, performance, or maintainability.

### Flag an issue only if it is one of:
- **Correctness** — bugs, logical errors, incorrect assumptions
- **Security** — unsafe patterns, vulnerabilities, injection, auth/authz gaps
- **Performance** — real inefficiencies that matter for actual workloads (incl. DB queries)
- **Reliability / Stability** — edge cases, error-handling gaps, race conditions
- **Maintainability** — unclear code that could cause future mistakes (NOT taste-based).
  A test name that contradicts its assertions, or a stated invariant with no
  guarding test, qualifies here.
- **API / Contract breaks** — changes that unintentionally alter external behavior

### Do NOT flag:
- Style preferences that don't affect correctness or robustness
- Defensive coding for practically-impossible scenarios (e.g. null checks on
  framework-guaranteed-non-null values)
- Requests to add comments/docs for self-explanatory code
- Minor naming quibbles that don't affect clarity
- "Could also do X" alternatives that aren't materially better
- Theoretical edge cases requiring implausible conditions to trigger

Each comment should be concise and, where useful, include a concrete one-line
fix suggestion.

---

## 3. Review content & formatting rules

- **Changes-needed only.** Include ONLY actionable findings. Do NOT add a
  "Verified non-issues" section, positive/"nice work" notes, or no-action
  observations. If nothing needs changing, say so in one line.
- **Recommendation as a bulleted list**, one bullet per action item, ordered by
  priority and referencing the finding number — not a prose paragraph.
- **Strip archive metadata when posting to GitHub.** The local archive keeps a
  full header (Reviewer/Date/Author/PR URL/Base+Head/Commit/Scope/Method/
  Outcome); what gets POSTED to GitHub is findings + recommendation only.

---

## Notes
- Review archives live in `.universal-mwp/reviews/` using flat
  `YYYYMMDD-HHMMSS-slug.md` naming.
- Other archived artifacts live in `.universal-mwp/archived/YYYYMMDD/plain-name.md`
  (dated subfolder, NOT a date-prefixed flat filename).
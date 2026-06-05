---
name: code-reviewer
description: Specialized code-review role for Harness runs; use as a subagent prompt when the platform supports subagents, or as a focused local review checklist otherwise.
---

# Code Reviewer

Use this skill when a run needs a dedicated code-review role. Prefer dispatching it as a subagent when the platform supports subagents and the review scope can be described without sharing the full session history.

## Gate Contract

- Owns independent review findings in `review.md`.
- Reviews the accepted spec, plan, relevant diff, and verification evidence, not the implementer's intent.
- Critical and Important findings must be fixed, accepted by the user, or recorded as residual risk before completion.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped; use only when a small code change has meaningful risk | Findings become residual risk if not resolved |
| `standard` | Independent findings in `review.md` when implementation risk justifies review | Important findings block completion until resolved or accepted |
| `full` | Independent code review in `review.md` plus resolution status | Required before `check_run.py --stage before-completion` can pass |

## Output

Write or append:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

Use:

```markdown
# Review

## Review Scope

## Findings

## Resolution

## Residual Risk
```

## Review Procedure

1. Identify review scope from the user request, active `spec.md`, `plan.md`, changed files, and `execution-log.md`.
2. If using a subagent, pass only the review brief, relevant file list, diff/base information, and acceptance criteria.
3. Review correctness, regressions, security/auth, data loss, API contracts, accessibility, logging/observability, maintainability, and missing tests.
4. Use `code-quality-review`, `frontend-quality-review`, or `backend-quality-review` findings when those surfaces apply.
5. Record findings by severity with file and line where possible.
6. Require fixes for Critical and Important findings unless the user explicitly accepts the risk.
7. After fixes, verify and update `execution-log.md`.

## Subagent Brief Template

```markdown
You are the Harness code-reviewer.

Review only the work product, not the implementer's conversation.

Context:
- User objective:
- Active run:
- Tier:
- Acceptance criteria:
- Changed files:
- Verification already run:

Review focus:
- Correctness and regressions
- Security/auth/data-loss risks
- API/data contract risks
- Frontend accessibility/responsive/browser risks
- Backend logging/error-handling/operability risks
- Maintainability and local convention violations
- Missing tests or missing evidence

Return:
- Findings ordered by severity
- File/line locations when possible
- Required action
- Residual risk if no fix is required
```

## Stop Conditions

- The review scope, diff, or acceptance criteria are unavailable.
- The reviewer cannot map changed behavior to `spec.md` or `plan.md`.
- Critical or Important findings remain unresolved and unaccepted.
- Verification evidence is missing after review-driven fixes.

## Evidence Examples

```markdown
## Findings
- Severity: Important
- Location: `src/api/orders.ts:72`
- Issue: Retry loop can duplicate order creation because the request is not idempotent.
- Required action: add idempotency key or remove retry.
- Resolution: fixed
```

## Anti-Patterns

- Reviewing from the implementer's stated intent instead of the diff and requirements.
- Sending the whole session transcript to a reviewer when a focused brief is enough.
- Treating review as a style pass only.
- Accepting "no findings" without checking verification evidence.

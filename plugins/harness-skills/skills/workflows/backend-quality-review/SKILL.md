---
name: backend-quality-review
description: Review backend, API, service, worker, persistence, and integration changes for boundaries, logging, error handling, and operability.
---

# Backend Quality Review

Use this skill for backend, API, service, worker, persistence, CLI, or integration changes after implementation and before completion.

## Gate Contract

- Owns backend-specific maintainability and operability findings in `review.md`.
- Composes with `code-quality-review`; use this skill for server-side boundary, logging, error handling, and data-safety checks.
- Critical and Important findings must be fixed, accepted by the user, or recorded as residual risk before completion.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped for tiny docs/config edits; record reason in `evaluation.md` when backend code changed but review is skipped | Skipped review becomes residual risk |
| `standard` | Backend review notes in `review.md` for API/service/data changes | Important findings block completion until resolved or accepted |
| `full` | Backend review plus verification evidence and resolution | Required before `check_run.py --stage before-completion` can pass |

## Output

Append to:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

Use:

```markdown
## Backend Quality Review

## Findings

## Verification Evidence

## Resolution

## Residual Risk
```

## Review Procedure

1. Identify changed backend entry points, services, data access, migrations, workers, integrations, and tests.
2. Check that controllers/handlers, services, repositories, jobs, and clients keep their local responsibilities.
3. Check input validation, authorization/permission boundaries, error handling, retries/timeouts, transactions, and data-shape compatibility where relevant.
4. Check logging/observability for external calls, state changes, background jobs, failures, and operationally important branches.
5. Check comments for non-obvious business rules, invariants, edge cases, or migration constraints.
6. Run relevant backend checks from `harness/tools/commands.md` and record command evidence.
7. Record findings, fixes, skipped checks, and residual risk.

## Quality Baseline

- Do not swallow errors or replace useful errors with vague success/failure summaries.
- Log meaningful operational events when the project has a logging facility; avoid noisy logs for every trivial branch.
- Keep API handlers thin when the project has service/data layers.
- Preserve schema, migration, permission, and compatibility expectations unless the spec explicitly changes them.
- Validate inputs at trust boundaries and document accepted residual risk when validation is deferred.
- Add comments for business rules and non-obvious constraints, not for obvious syntax.

## Stop Conditions

- Error handling, logging, or data-safety behavior cannot be determined for changed backend paths.
- Important operational failures have no logs, tests, or documented manual verification.
- A suggested fix changes API/data behavior outside the accepted spec.
- Critical or Important findings remain unresolved and unaccepted.

## Evidence Examples

```markdown
## Backend Quality Review

## Findings
- Severity: Important
- Location: `src/orders/service.ts:88`
- Issue: Payment provider errors are caught and returned as generic success state; no log preserves provider error context.
- Required action: log structured failure context and return an explicit error path.
- Resolution: fixed

## Verification Evidence
- Command: npm test -- orders
- Result: passed
```

## Anti-Patterns

- Assuming backend code is acceptable because the UI happy path works.
- Adding comments everywhere while leaving business rules and failure modes unexplained.
- Logging secrets or sensitive payloads instead of safe diagnostic context.
- Letting handlers grow into mixed validation, persistence, integration, and formatting modules.

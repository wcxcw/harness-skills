---
name: code-quality-review
description: Review completed code changes for maintainability, structure, observability, comments, and local conventions before final verification.
---

# Code Quality Review

Use this skill after implementation and before final verification when a task changes application code. It complements correctness review by checking whether the implementation is maintainable in this repository.

## Gate Contract

- Owns maintainability findings in `review.md` or a clearly labeled `Code Quality Review` section.
- Uses `harness/context/coding-conventions.md` when present, but reads it only when the task changes code or the current review needs project-specific conventions.
- Critical and Important code-quality findings must be fixed, accepted by the user, or recorded as residual risk before completion.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped for documentation/config-only work; record reason in `evaluation.md` when code changed but review is skipped | Skipped review becomes residual risk |
| `standard` | Code-quality notes in `review.md` when application code changed | Important findings block completion until resolved or accepted |
| `full` | Code-quality review in `review.md` plus resolution | Required before `check_run.py --stage before-completion` can pass |

## Output

Append to the active run's review artifact:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

Recommended section:

```markdown
## Code Quality Review

## Findings

## Resolution

## Residual Risk
```

## Review Procedure

1. Identify changed files from the diff, `plan.md`, and `execution-log.md`.
2. Read the smallest needed project conventions, usually `harness/context/coding-conventions.md` plus nearby existing code patterns.
3. Check whether the implementation preserves local module boundaries and existing abstractions.
4. Check whether complexity matches the task size and whether large files, mixed responsibilities, or speculative abstractions were introduced.
5. Check error handling, logging/observability, comments for non-obvious business rules, and testability.
6. Record findings with severity and file location when possible.
7. Fix Critical and Important findings or record the user-accepted residual risk.
8. Re-run relevant verification and append evidence to `execution-log.md`.

## Quality Baseline

- Prefer existing project patterns over new structures unless the spec requires a new pattern.
- Keep root application files, controllers, services, and page components focused on orchestration rather than mixed UI, state, data access, and business logic.
- Split code when a file gains unrelated responsibilities, repeated logic, or hard-to-test branches.
- Add runtime logs for important side effects, external calls, background jobs, state changes, and exceptional paths when the project has logging facilities.
- Add comments only for non-obvious business rules, edge cases, invariants, tradeoffs, or integration constraints.
- Do not hide missing tests, lint failures, build failures, or skipped checks behind a positive summary.

## Stop Conditions

- Project conventions or changed files are unavailable.
- The diff cannot be mapped back to the accepted spec or plan.
- Critical or Important findings remain unresolved and unaccepted.
- Verification evidence for the fixed findings is missing.

## Evidence Examples

```markdown
## Code Quality Review

## Findings
- Severity: Important
- Location: `src/App.vue:1`
- Issue: Root component now owns routing, API calls, filtering state, and modal behavior.
- Required action: split feature state/API calls into composables and extract repeated UI into components.
- Resolution: fixed

## Residual Risk
None.
```

## Anti-Patterns

- Treating "the feature works" as sufficient when the implementation is hard to maintain.
- Calling every maintainability issue "style" and deferring it without risk recording.
- Adding broad abstractions that the current spec does not need.
- Adding comments that describe obvious syntax instead of clarifying decisions.

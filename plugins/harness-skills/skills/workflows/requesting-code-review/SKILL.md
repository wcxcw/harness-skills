---
name: requesting-code-review
description: Review completed changes before final verification and record findings in `review.md`.
---

# Requesting Code Review

Use this skill after implementation and before final completion.

## Gate Contract

- Owns `review.md` for `full` tier runs and any run with meaningful implementation risk.
- `full` tier runs require `review.md` before `check_run.py --stage before-completion` can pass.
- Review findings must be fixed or explicitly accepted as residual risk before final verification.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped; document reason in `evaluation.md` when skipped | No review artifact gate |
| `standard` | `review.md` when risk justifies it | Review gaps become residual risk |
| `full` | `review.md` with findings and resolution | Required before `check_run.py --stage before-completion` can pass |

## Output

Save review results to:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

## Required Sections

```markdown
# Review

## Review Scope

## Findings

## Resolution

## Residual Risk
```

## Review Procedure

1. Identify the review base: user request, `spec.md`, `plan.md`, and relevant diff.
2. Review the change as a fresh reader. Do not rely on implementation intent.
3. Prioritize correctness, regressions, missing tests, security, data loss, concurrency, accessibility, and scope creep.
4. Record findings by severity with file and line when possible.
5. Fix Critical and Important findings before continuing, or record why the user accepted the risk.
6. Re-run relevant verification and append evidence to `execution-log.md`.

If no findings exist, state that explicitly and record remaining test gaps.

## Finding Format

```markdown
- Severity: Critical | Important | Minor
- Location: `path/to/file:line`
- Issue: [behavioral risk]
- Required action: [fix, test, or accepted risk]
- Resolution: fixed | accepted | deferred
```

## Stop Conditions

- The diff, requirements, or verification evidence is not available.
- Critical or Important findings are unresolved and not explicitly accepted by the user.
- Review scope excludes changed behavior that affects acceptance criteria.
- The reviewer cannot map changes back to `spec.md` or `plan.md`.

## Evidence Examples

```markdown
## Findings
- Severity: Important
- Location: `harness/scripts/check_run.py:82`
- Issue: `standard` tier does not reject unresolved `Needs decision`.
- Required action: add marker check and regression test.
- Resolution: fixed
```

## Anti-Patterns

- Reviewing only style when behavior changed.
- Accepting "no findings" without checking tests and acceptance criteria.
- Treating review as final verification.
- Deferring important findings without recording residual risk.

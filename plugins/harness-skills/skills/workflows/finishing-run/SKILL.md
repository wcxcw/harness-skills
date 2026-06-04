---
name: finishing-run
description: Close an active harness run with `evaluation.md`, residual risk, and harness feedback.
---

# Finishing Run

Use this skill at the end of a run, after verification.

## Gate Contract

- Owns `evaluation.md`.
- `xs`, `standard`, and `full` tier runs require `evaluation.md` before `check_run.py --stage before-completion` can pass.
- The run is not complete until local gates pass or the user explicitly accepts documented residual risk.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | `evaluation.md` with acceptance and risk | Required before completion |
| `standard` | `evaluation.md` summarizing spec, plan, and execution evidence | Required before completion |
| `full` | `evaluation.md` summarizing design, review, verification, and feedback | Required before completion |

## Output

Save:

```text
harness/runs/YYYY-MM-DD-short-task-name/evaluation.md
```

## Required Sections

```markdown
# Evaluation

## Acceptance

## Verification

## Review Status

## Residual Risk

## Harness Feedback
```

If the run exposed missing commands, stale context, unclear gates, or weak skills, record the proposed harness update. Update canonical harness files only when the workflow or user explicitly allows it.

Before final response, run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier xs|standard|full` when available and record the result in `evaluation.md`.

## Stop Conditions

- Acceptance, verification, review status, or residual risk is unknown.
- The final gate has not run or has failed.
- The run revealed harness feedback but it is not recorded.
- The user has not accepted a known residual risk that blocks completion.

## Evidence Examples

```markdown
## Verification
- Final gate: `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard`
- Result: passed

## Residual Risk
- None.
```

## Anti-Patterns

- Ending with a summary but no `evaluation.md`.
- Hiding skipped checks in prose instead of recording them.
- Updating canonical harness files without evidence or permission.
- Treating harness feedback as optional when the run exposed a process gap.

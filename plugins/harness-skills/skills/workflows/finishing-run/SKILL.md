---
name: finishing-run
description: Close an active harness run with `evaluation.md`, residual risk, and harness feedback.
---

# Finishing Run

Use this skill at the end of a run in two steps: draft the evaluation after implementation and review, then finalize it after verification. The draft must exist before the completion gate runs.

## Gate Contract

- Owns `evaluation.md`.
- Owns the final lifecycle transition from the current session's run to `verifying`; the Stop hook closes it only after fresh gates pass.
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

First create `evaluation.md` with the acceptance, current verification evidence, review status, residual risk, and feedback. Mark unfinished verification as pending; do not claim it passed. Next run `verification-before-completion` to check the final task evidence and completion gate. Update the evaluation with the actual verification and gate result; when this update changes final evidence, rerun the gate against the updated artifact.

Before final response, run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier <xs|standard|full>` when available and record the result in `evaluation.md`. The local checker checks recorded evidence structure; passing it does not independently establish that behavior works or that review was independent.

After all run artifacts are final and that command passes, immediately run:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --tier <xs|standard|full> --set-phase verifying
```

Do not set `verifying` for progress updates or ordinary conversation. The
session-scoped Stop hook rechecks the run and writes `closed` on success. If the
platform has no Harness Stop hook, explicitly set `closed` after the final gate.

## Stop Conditions

- Acceptance, verification, review status, or residual risk is unknown.
- The final gate has not run or has failed.
- The run is not bound to the current session or was armed as `verifying` before artifacts became final.
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
- Leaving a completed run as `active`/`reviewing`, or arming `verifying` during an interim response.
- Hiding skipped checks in prose instead of recording them.
- Updating canonical harness files without evidence or permission.
- Treating harness feedback as optional when the run exposed a process gap.

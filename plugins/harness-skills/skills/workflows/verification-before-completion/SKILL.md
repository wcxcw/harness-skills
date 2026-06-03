---
name: verification-before-completion
description: Verify required evidence before claiming completion and make skipped checks explicit.
---

# Verification Before Completion

Use this skill after implementation and review.

## Gate Contract

- Owns the final evidence check across `execution-log.md`, `review.md`, and `evaluation.md`.
- Must run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier xs|standard|full` when the checker exists.
- Completion claims require fresh evidence from this run, not assumptions from earlier attempts.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | `execution-log.md` and `evaluation.md` evidence | Required before completion |
| `standard` | Evidence mapped to `spec.md` and `plan.md` | Required before completion |
| `full` | Evidence plus `review.md` resolution | Required before completion |

## Rules

- Read `spec.md`, `plan.md`, `execution-log.md`, and `review.md`.
- Run approved commands from `harness/tools/commands.md`.
- Confirm each acceptance criterion has evidence.
- Record skipped checks and reasons.
- Read command output and exit codes before reporting pass/fail.
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier xs|standard|full` when available.
- Do not claim completion while verification is missing or failing unless the risk is explicitly documented and accepted.

## Evidence Checklist

- Every acceptance criterion in `spec.md` has a matching command or manual check.
- Every task verification in `plan.md` is represented in `execution-log.md`.
- Every review finding in `review.md` is fixed, accepted, or deferred with a reason.
- `evaluation.md` summarizes acceptance, verification, review status, and residual risk.
- The final local gate passed, or the failure is explicitly documented and not presented as complete.

## Stop Conditions

- A required command has not been run in the current run.
- Command output or exit status is unavailable.
- Acceptance criteria do not map to evidence.
- `check_run.py --stage before-completion` fails.

## Evidence Examples

```markdown
## Final Verification

- Command: `python3 harness/scripts/check_run.py harness/runs/2026-06-03-demo --stage before-completion --tier full`
- Result: passed
- Acceptance covered: all criteria in `spec.md`
- Skipped checks: none
```

## Anti-Patterns

- Saying "should pass" or "looks good" without fresh output.
- Reporting only the command name without the result.
- Ignoring skipped checks.
- Claiming completion while the final gate is failing.

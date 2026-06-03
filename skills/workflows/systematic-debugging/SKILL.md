---
name: systematic-debugging
description: Diagnose and fix bugs by reproducing, isolating cause, fixing narrowly, and adding regression evidence.
---

# Systematic Debugging

Use this skill for bug reports, failing tests, regressions, or unexplained runtime behavior.

## Gate Contract

- Owns debugging evidence in `execution-log.md` and the bug contract inside `spec.md`.
- The fix cannot be complete until `check_run.py --stage before-completion` passes for the selected tier or the unresolved risk is documented in `evaluation.md`.
- Local gates decide continuation; a plausible root cause is not enough.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Reproduction or manual diagnostic evidence in `execution-log.md` | Required before completion |
| `standard` | Bug behavior in `spec.md`, fix evidence in `execution-log.md` | Required before completion |
| `full` | `spec.md`, regression evidence, `review.md`, `evaluation.md` | Required before final gate can pass |

## Flow

1. Read the full error, stack trace, failing output, or bug report. Record the exact symptom.
2. Reproduce the issue or record why reproduction is not possible.
3. Capture observed behavior, expected behavior, scope, and acceptance criteria in `spec.md`.
4. Inspect recent changes, similar working code, configuration, and data flow before proposing a fix.
5. State one root-cause hypothesis and the evidence for it.
6. Test the hypothesis with the smallest diagnostic change or command.
7. Add a regression test or equivalent manual check before applying the fix.
8. Apply the smallest fix that addresses the root cause.
9. Verify the original issue and adjacent behavior.
10. Record commands, failures, hypothesis changes, and final evidence in `execution-log.md`; record residual risk in `evaluation.md`.

## Stop Conditions

- If reproduction is impossible, stop and request or gather more evidence.
- If three fix attempts fail, stop and reassess the architecture or premise before adding another patch.
- If a fix requires broad refactoring, update `spec.md` and `plan.md` before continuing.

## Evidence Examples

```markdown
## Debugging: missing run artifact not reported

- Symptom: `check_run.py --stage before-implementation` exits 0 when `spec.md` is missing.
- Reproduction: `python3 harness/scripts/check_run.py harness/runs/demo --stage before-implementation`
- Hypothesis: required file list skips `spec.md` for standard tier.
- Diagnostic: inspect `check_before_implementation()`.
- Fix evidence: unit test fails before fix and passes after fix.
```

## Anti-Patterns

- Proposing a fix before reproduction or root-cause evidence.
- Changing multiple variables in one diagnostic step.
- Treating a symptom patch as root-cause resolution.
- Trying a fourth fix after three failures without reassessing the design.

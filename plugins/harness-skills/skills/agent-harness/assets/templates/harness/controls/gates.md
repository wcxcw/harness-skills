# Gates

Gates turn harness guidance into checks. Agents should use these gates before implementation and before completion.

## Tiers

| Tier | Use for | Required run artifacts |
| --- | --- | --- |
| `xs` | tiny docs/config/single-file changes with no product or technical decisions | `execution-log.md`, `evaluation.md` |
| `standard` | normal feature work, contained bugfixes, and multi-file changes | `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `evaluation.md` |
| `full` | greenfield work, new product/feature direction, architecture/data/security/CI/dependency risk | `workflow.md`, `design.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, `evaluation.md` |

## Run Boundary

One run should cover the full lifecycle of one user objective, including
follow-up corrections and verification requested before acceptance. Do not
create a new run for a small fix to the same objective. Create a new run when
the objective changes, scope materially expands, the previous run is closed, or
the user explicitly starts another task.

## Before Implementation

For `standard` and `full` runs, the active run must pass these checks before editing application code:

- `harness/runs/<run>/spec.md` exists.
- `harness/runs/<run>/plan.md` exists.
- `harness/runs/<run>/workflow.md` exists and records skills used plus gate status.
- `harness/runs/<run>/design.md` exists for `full` runs.
- `spec.md` contains objective, scope, non-goals, acceptance criteria, verification, and open questions.
- `plan.md` contains ordered tasks and verification.
- `spec.md` and `plan.md` do not contain unresolved blocking markers such as `Needs decision` or `TBD`.

Recommended local check:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard
```

## Before Completion

The active run must pass these checks before claiming completion:

- `execution-log.md` exists.
- `review.md` exists and records review findings or "none" for `full` runs.
- `evaluation.md` exists.
- `execution-log.md` records commands or manual checks and their results.
- `evaluation.md` records acceptance status, residual risk, and harness feedback.
- Skipped verification is explicitly explained.

Recommended local check:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard
```

## Gate Failures

- If a gate fails because a decision is missing, stop implementation and resolve the decision.
- If a gate fails because evidence is missing, run the relevant verification or record why it cannot be run.
- If a gate is not applicable, record the reason in the active run.

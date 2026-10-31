# Gates

Gates turn harness guidance into checks. Agents should use these gates before implementation and before completion.
Use `harness/controls/risk-matrix.md` when risk affects tier choice, review depth, or verification scope.

## Pre-Run Alignment

When the objective or material decisions are unclear, do not create a run yet. Invite the user to explicitly invoke `$grilling`, which asks one decision question at a time and creates no files. After the user confirms shared understanding, create the run and record that confirmation in `spec.md`.

## Tiers

Run tiers apply only when a run is warranted. A no-run micro change is allowed
only when the request is explicit, local to one surface or nearby file area,
behavior-preserving, decision-free, easy to verify with one targeted check, and
locally reversible. Examples: typo fixes, one sentence of copy, one named
selector font-size change, or one spacing/color token. Not micro: broad visual
improvements, typography hierarchy changes, cross-page changes, behavior
changes, or work requiring a design/product/technical decision.

| Tier | Use for | Required run artifacts |
| --- | --- | --- |
| `xs` | small changes that still need a run record, such as low-risk config/docs/code edits with verification evidence | `execution-log.md`, `evaluation.md` |
| `standard` | normal feature work, contained bugfixes, and multi-file changes | `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `evaluation.md` |
| `full` | greenfield work, new product/feature direction, architecture/data/security/CI/dependency risk | `input.md`, `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, `evaluation.md` |

Each tier also records `run-state.json` when session binding is supported. This is the workflow contract; the checker does not verify every listed artifact or the truth of its contents.

## Run Boundary

One run should cover one user objective, including subsequent corrections,
small adjustments, and additional verification. When no run is active, first
check whether the change meets all no-run micro criteria above; if so, edit
directly. Otherwise, if the relevant run is closed,
explicitly resume it and bind it to the current session before continuing;
append this round's review and verification evidence, update `evaluation.md`
without erasing history, and rerun applicable completion gates. Do not reuse
old conclusions as evidence for new changes. A resumed run retains its original
Git baseline, which may include unrelated commits; check the actual change
scope. Identify the run from task context, not directory recency; do not
overwrite a run active in another session. Closure
alone is not a reason to create a new run. Create a new run when the objective
changes, scope materially expands, or the user requests a separate record.

## Before Implementation

For `standard` and `full` runs, the active run must pass these checks before editing application code:

- `harness/runs/<run>/spec.md` exists.
- `harness/runs/<run>/plan.md` exists.
- `harness/runs/<run>/workflow.md` exists and records skills used plus gate status.
- `spec.md` contains alignment, objective, scope, non-goals, acceptance criteria, verification, and open questions.
- `spec.md` records alignment and its source. A clear user request can establish alignment for the decisions it actually specifies; record that source without asking for duplicate confirmation. Resolve material unanswered decisions before implementation.
- `plan.md` contains ordered tasks and verification.
- `spec.md` and `plan.md` do not contain unresolved blocking markers such as `Needs decision` or `TBD`.

Recommended local check:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard
```

## Before Completion

The active run must pass these checks before claiming completion:

- `execution-log.md` exists.
- `review.md` exists for `full` runs and contains the semantic sections `Review Scope`, `Findings`, `Resolution`, and `Residual Risk` (or their documented Chinese aliases).
- `evaluation.md` exists.
- `execution-log.md` records commands or manual checks and their results.
- Application code changes received code-quality review, frontend/backend quality review when applicable, or the skip reason is recorded.
- Critical and Important review findings are fixed, explicitly accepted by the user, or recorded as residual risk.
- `evaluation.md` records acceptance status, residual risk, and harness feedback.
- Skipped verification is explicitly explained.
- The Stop hook is only a final safety recheck for a same-session run explicitly marked `verifying`; it does not scan the latest historical run.

Recommended local check:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard
```

## Gate Failures

- If a gate fails because a decision is missing, stop implementation and resolve the decision.
- If a gate fails because evidence is missing, run the relevant verification or record why it cannot be run.
- If a gate is not applicable, record the reason in the active run.

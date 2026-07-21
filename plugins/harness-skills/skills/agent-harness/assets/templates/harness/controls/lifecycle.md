# Lifecycle

The harness lifecycle is the closed loop for agentic work. Workflow skills can help execute each stage, but local gates decide whether the run may continue.

Before this lifecycle starts, the user may explicitly invoke `$grilling` to resolve an unclear idea. Grilling is conversational, creates no artifacts, and must finish with explicit shared-understanding confirmation before a run is created.

## Stages

| Stage | Workflow skill | Required artifact | Gate |
| --- | --- | --- | --- |
| Spec | `writing-specs` | `workflow.md`, `spec.md` | User-confirmed alignment and no unresolved blocking decisions |
| Plan | `writing-plans` | `plan.md` | Tasks map to acceptance criteria |
| Preflight | `agent-harness` | Gate output | `check_run.py --stage before-implementation` passes |
| Execute | `executing-plans`, `test-driven-development`, or `systematic-debugging` | `execution-log.md` | Verification evidence recorded |
| Review | `requesting-code-review` | `review.md` | Review findings addressed or documented |
| Verify | `verification-before-completion` | `execution-log.md` | Commands/manual checks recorded |
| Finish | `finishing-run` | `evaluation.md` | `check_run.py --stage before-completion` passes |
| Improve | `agent-harness` or `writing-skills` | Harness update proposal | Feedback captured before canonical changes |

## Run Artifact Contract

Use the smallest tier that safely controls the work:

Do not create a run for a micro change when no active run exists. It must be
explicit, local to one surface or nearby file area, behavior-preserving,
decision-free, easy to verify with one targeted check, and locally reversible.
Examples include typo fixes, one sentence of copy, one named selector font-size
change, or one spacing/color token. Broad visual improvements, typography
hierarchy changes, cross-page changes, behavior changes, or work requiring a
design/product/technical decision are not micro changes.

A run represents a user objective. It is not a record for every individual
agent attempt, patch, or follow-up message. When the user asks for corrections,
test fixes, extra verification, or small adjustments that still target the same
objective, continue the active run and append the new evidence to its artifacts.

Create a new run only when the objective changes, the requested scope
materially expands, the previous run has been accepted and closed, or the user
explicitly starts a new task.

### XS

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

### Standard

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

### Full

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
└── evaluation.md
```

New runs record confirmed product and technical decisions directly in `spec.md`. Legacy `design.md` files may still be read when referenced. Use `review.md` for `full` runs or when risk justifies review.

## Continuation Rule

Do not advance to the next stage when the required artifact or gate is missing.
If a stage is intentionally skipped, record the reason in `workflow.md` and make
sure the next gate still passes. Follow-up work for the same objective remains
in the active run; update `plan.md`, `execution-log.md`, or `evaluation.md`
instead of creating a sibling run.

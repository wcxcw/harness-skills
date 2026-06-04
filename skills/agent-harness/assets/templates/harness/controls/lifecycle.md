# Lifecycle

The harness lifecycle is the closed loop for agentic work. Workflow skills can help execute each stage, but local gates decide whether the run may continue.

## Stages

| Stage | Workflow skill | Required artifact | Gate |
| --- | --- | --- | --- |
| Intake | `brainstorming` | `workflow.md`, `design.md` | User-approved direction |
| Spec | `writing-specs` | `spec.md` | No unresolved blocking decisions |
| Plan | `writing-plans` | `plan.md` | Tasks map to acceptance criteria |
| Preflight | `agent-harness` | Gate output | `check_run.py --stage before-implementation` passes |
| Execute | `executing-plans`, `test-driven-development`, or `systematic-debugging` | `execution-log.md` | Verification evidence recorded |
| Review | `requesting-code-review` | `review.md` | Review findings addressed or documented |
| Verify | `verification-before-completion` | `execution-log.md` | Commands/manual checks recorded |
| Finish | `finishing-run` | `evaluation.md` | `check_run.py --stage before-completion` passes |
| Improve | `agent-harness` or `writing-skills` | Harness update proposal | Feedback captured before canonical changes |

## Run Artifact Contract

Use the smallest tier that safely controls the work:

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
├── design.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
└── evaluation.md
```

Use `design.md` for new feature, greenfield, or product direction work. Narrow bugfixes may skip `design.md` when `spec.md` includes reproduction, expected behavior, and scope. Use `review.md` for `full` runs or when risk justifies review.

## Continuation Rule

Do not advance to the next stage when the required artifact or gate is missing.
If a stage is intentionally skipped, record the reason in `workflow.md` and make
sure the next gate still passes. Follow-up work for the same objective remains
in the active run; update `plan.md`, `execution-log.md`, or `evaluation.md`
instead of creating a sibling run.

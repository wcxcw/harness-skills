# Agents.md

This file is the index for the project Agent Harness. It points agents and humans to the canonical files that define the task target, available context, executable tools, feedback loop, safety boundaries, and evaluation criteria.

## Harness Stack

| Layer | Purpose | File |
| --- | --- | --- |
| Spec | Feature task template | [harness/specs/feature-template.md](harness/specs/feature-template.md) |
| Spec | Bugfix task template | [harness/specs/bugfix-template.md](harness/specs/bugfix-template.md) |
| Context | Repository map | [harness/context/repo-map.md](harness/context/repo-map.md) |
| Context | Architecture notes | [harness/context/architecture.md](harness/context/architecture.md) |
| Context | Coding conventions | [harness/context/coding-conventions.md](harness/context/coding-conventions.md) |
| Context | Dependency notes | [harness/context/dependency-notes.md](harness/context/dependency-notes.md) |
| Tools | Approved commands | [harness/tools/commands.md](harness/tools/commands.md) |
| Tools | Verification process | [harness/tools/verification.md](harness/tools/verification.md) |
| Feedback | Run records | [harness/runs/](harness/runs/) |
| Guardrails | Permission rules | [harness/guardrails/permissions.md](harness/guardrails/permissions.md) |
| Guardrails | Work boundaries | [harness/guardrails/boundaries.md](harness/guardrails/boundaries.md) |
| Guardrails | Rollback process | [harness/guardrails/rollback.md](harness/guardrails/rollback.md) |
| Evaluation | Acceptance checklist | [harness/evals/acceptance-checklist.md](harness/evals/acceptance-checklist.md) |
| Evaluation | Regression checklist | [harness/evals/regression-checklist.md](harness/evals/regression-checklist.md) |
| Evaluation | Task scorecard | [harness/evals/task-scorecard.md](harness/evals/task-scorecard.md) |

## Run Convention

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

## Agent Workflow

1. Read the active run's `spec.md` and `plan.md`.
2. Load only the needed context files.
3. Check guardrails before editing.
4. Execute one small task at a time.
5. Run approved verification commands.
6. Record results in the run directory.
7. Update evaluation before handoff.

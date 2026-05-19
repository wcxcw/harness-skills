# AGENTS.md

This file is the index for the project Agent Harness. It points agents and humans to the canonical files that define the task target, available context, executable tools, feedback loop, safety boundaries, and evaluation criteria.

## Harness Stack

| Layer | Purpose | File |
| --- | --- | --- |
| Spec | Feature task template | [harness/specs/feature-template.md](harness/specs/feature-template.md) |
| Spec | Bugfix task template | [harness/specs/bugfix-template.md](harness/specs/bugfix-template.md) |
| Context | Project brief | [harness/context/project-brief.md](harness/context/project-brief.md) |
| Context | Initialization notes | [harness/context/initialization-notes.md](harness/context/initialization-notes.md) |
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

## Initialization Mode

- `greenfield`: New project or one-sentence project idea. Start from `project-brief.md`, `initialization-notes.md`, and the active run's `idea.md` when present.
- `brownfield`: Existing codebase. Start from `harness/context/*`, existing README/config/CI/package files, then the active run.
- `existing-harness`: Existing `AGENTS.md` or `harness/`. Preserve current harness content unless the user asks for a rewrite.

## Run Convention

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── idea.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Use `idea.md` only when the task started as a raw idea and used `idea-refine`.

## Agent Workflow

1. Determine the initialization mode from `harness/context/initialization-notes.md`.
2. For greenfield work, read `project-brief.md`, then the active run's `idea.md`, `spec.md`, and `plan.md`.
3. For brownfield work, read needed files under `harness/context/`, then existing project documentation/configuration, then the active run.
4. Load only the needed context files.
5. Check guardrails before editing.
6. Execute one small task at a time.
7. Run approved verification commands.
8. Record results in the run directory.
9. Update evaluation before handoff.
10. Review `Context Updates`, `execution-log.md`, and `evaluation.md` for harness gaps.
11. Update canonical harness files only when the user asked for harness maintenance, the active workflow explicitly allows it, or the update is a factual correction from repository evidence. Otherwise, list proposed harness updates for confirmation.

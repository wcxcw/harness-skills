# AGENTS.md

This file is the index for the project Agent Harness. It points agents and humans to the canonical files that define the task target, available context, executable tools, feedback loop, safety boundaries, and evaluation criteria.

## Harness Stack

| Layer | Purpose | File |
| --- | --- | --- |
| Context | Project brief | [harness/context/project-brief.md](harness/context/project-brief.md) |
| Context | Initialization notes | [harness/context/initialization-notes.md](harness/context/initialization-notes.md) |
| Tools | Approved commands | [harness/tools/commands.md](harness/tools/commands.md) |
| Feedback | Verification process | [harness/feedback/verification.md](harness/feedback/verification.md) |
| Feedback | Run records | [harness/runs/](harness/runs/) |
| Guardrails | Work boundaries | [harness/guardrails/boundaries.md](harness/guardrails/boundaries.md) |
| Evaluation | Task scorecard | [harness/evals/task-scorecard.md](harness/evals/task-scorecard.md) |

## Optional Harness Files

Create these only when the project needs them:

- Brownfield context: `harness/context/repo-map.md`, `harness/context/architecture.md`, `harness/context/coding-conventions.md`, `harness/context/dependency-notes.md`
- Extra guardrails: `harness/guardrails/permissions.md`, `harness/guardrails/rollback.md`
- Extra evals: `harness/evals/acceptance-checklist.md`, `harness/evals/regression-checklist.md`
- Spec templates: `harness/specs/feature-template.md`, `harness/specs/bugfix-template.md`

## Initialization Mode

- `greenfield`: New project or one-sentence project idea. Start from `project-brief.md`, `initialization-notes.md`, and the active run's `idea.md` when present.
- `brownfield`: Existing codebase. Start from available `harness/context/*`, existing README/config/CI/package files, then the active run.
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

## Operating Principles

- Clarify before coding: convert vague requests into explicit goals, constraints, and success criteria.
- Confirm blocking decisions before implementation: technology stack, runtime, data model, core architecture, external services, deployment target, and major UX/platform choices must be confirmed or explicitly deferred as non-coding decision tasks.
- Spec before implementation: use the active run's `spec.md` for non-trivial work.
- Plan into small verifiable tasks: each task should include scope, likely files, dependencies, and verification.
- Evidence before completion: record commands, checks, failures, and skipped verification in the active run.
- Keep scope small: avoid unrelated refactors, speculative abstractions, and behavior outside the spec.
- Improve the harness from evidence: feed repeated failures or missing context back into canonical harness files.

## Implementation Gate

Do not write application code when `spec.md` or `plan.md` still has unresolved blocking questions. Blocking questions include technology stack, framework, runtime, data model, authentication, external services, deployment target, and core user-facing behavior.

If the user wants to defer a decision, make that decision the first non-coding task in `plan.md`. Resolve it before implementation tasks begin.

## Agent Workflow

1. Determine the initialization mode from `harness/context/initialization-notes.md`.
2. For greenfield work, read `project-brief.md`, then the active run's `idea.md`, `spec.md`, and `plan.md`.
3. For brownfield work, read needed files under `harness/context/`, then existing project documentation/configuration, then the active run.
4. Load only the needed context files.
5. Check guardrails before editing.
6. Confirm there are no unresolved blocking questions before editing application code.
7. Execute one small task at a time.
8. Run approved verification commands.
9. Record evidence in the run directory before claiming completion.
10. Update evaluation before handoff.
11. Review `Context Updates`, `execution-log.md`, and `evaluation.md` for harness gaps.
12. Update canonical harness files only when the user asked for harness maintenance, the active workflow explicitly allows it, or the update is a factual correction from repository evidence. Otherwise, list proposed harness updates for confirmation.

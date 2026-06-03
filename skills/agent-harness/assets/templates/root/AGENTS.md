# AGENTS.md

This file is the index for the project Agent Harness. It points agents and humans to the canonical files that define the task target, available context, executable tools, feedback loop, safety boundaries, and evaluation criteria.

## Harness Stack

| Layer | Purpose | File |
| --- | --- | --- |
| Context | Project brief | [harness/context/project-brief.md](harness/context/project-brief.md) |
| Context | Initialization notes | [harness/context/initialization-notes.md](harness/context/initialization-notes.md) |
| Controls | Local gates | [harness/controls/gates.md](harness/controls/gates.md) |
| Controls | Closed-loop lifecycle | [harness/controls/lifecycle.md](harness/controls/lifecycle.md) |
| Controls | Skill compatibility | [harness/controls/skills.md](harness/controls/skills.md) |
| Tools | Approved commands | [harness/tools/commands.md](harness/tools/commands.md) |
| Feedback | Verification process | [harness/feedback/verification.md](harness/feedback/verification.md) |
| Feedback | Run records | [harness/runs/](harness/runs/) |
| Guardrails | Work boundaries | [harness/guardrails/boundaries.md](harness/guardrails/boundaries.md) |
| Evaluation | Task scorecard | [harness/evals/task-scorecard.md](harness/evals/task-scorecard.md) |
| Scripts | Run gate checker | [harness/scripts/check_run.py](harness/scripts/check_run.py) |

## Initialization Mode

- `greenfield`: New project or one-sentence project idea. Start from `project-brief.md`, `initialization-notes.md`, and the active run's `workflow.md` and `design.md` when present.
- `brownfield`: Existing codebase. Start from available `harness/context/*`, existing README/config/CI/package files, then the active run.
- `existing-harness`: Existing `AGENTS.md` or `harness/`. Preserve current harness content unless the user asks for a rewrite.

## Language Policy

- Use the user's main language for generated harness content.
- If the user describes the project in Chinese, write `workflow.md`, `design.md`, `spec.md`, `plan.md`, run records, and harness context in Chinese.
- Keep code identifiers, commands, file paths, library names, framework names, and API names in their original language.
- For existing projects, prefer the project's established documentation language when it is consistent.

## Run Convention

Use the smallest tier that safely controls the work.

XS:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

Standard:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Full:

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

Use `design.md` for new feature, greenfield, or product direction work. Use `review.md` for `full` runs or when risk justifies review. Use `idea.md` only for legacy runs that started before the workflow layer existed.

## Operating Principles

- Clarify before coding: convert vague requests into explicit goals, constraints, and success criteria.
- Confirm product shape before implementation: target audience, core workflow, information architecture, content/data sources, update model, and MVP quality bar must be explicit for product or content-driven projects.
- Confirm blocking decisions before implementation: technology stack, runtime, data model, core architecture, external services, deployment target, and major UX/platform choices must be confirmed or explicitly deferred as non-coding decision tasks.
- Spec before implementation: use the active run's `spec.md` for non-trivial work.
- Plan into small verifiable tasks: each task should include scope, likely files, dependencies, and verification.
- Check local gates before implementation and before completion.
- Evidence before completion: record commands, checks, failures, and skipped verification in the active run.
- Keep scope small: avoid unrelated refactors, speculative abstractions, and behavior outside the spec.
- Improve the harness from evidence: feed repeated failures or missing context back into canonical harness files.
- Treat canonical harness files as repository-owned collaboration assets.

## Collaboration and Version Control

- Commit canonical harness files: `AGENTS.md`, `harness/context/`, `harness/tools/`, `harness/feedback/`, `harness/guardrails/`, and `harness/evals/`.
- Treat `harness/runs/` as task-owned records. Commit only run directories that are useful for review, audit, onboarding, future context, architecture decisions, or complex bug investigations.
- Do not use personal local harness copies as the source of truth. Shared agent behavior should come from the repository harness.
- During normal feature or bugfix work, record harness improvement proposals in the active run's `evaluation.md`; do not directly edit canonical harness files unless the workflow explicitly allows it.
- Modify canonical harness files only for explicit harness maintenance, user-requested harness initialization/improvement, or factual corrections from repository evidence.
- In multi-person repositories, protect `AGENTS.md` and canonical `harness/` directories with review rules or CODEOWNERS when practical.
- If most run records should stay local, ignore `harness/runs/*` while preserving `harness/runs/.gitkeep`, then force-add selected run directories when needed.

## Guided Initialization

When the project only has a one-sentence idea, product shape is unclear, technology choices are missing, or the user wants to discuss direction first, do not write application code. Use `brainstorming` to ask focused questions and produce `design.md`.

After the user answers, update `project-brief.md` and `initialization-notes.md`, then create or update `workflow.md`, `design.md`, `spec.md`, and `plan.md`. If a blocking decision remains unresolved, make it the first non-coding task in `plan.md`.

## Implementation Gate

Do not write application code when `spec.md` or `plan.md` still has unresolved blocking questions. Blocking questions include target audience, content/data scope, information architecture, core UX, success criteria, technology stack, framework, runtime, data model, authentication, external services, deployment target, and core user-facing behavior.

If the user wants to defer a decision, make that decision the first non-coding task in `plan.md`. Resolve it before implementation tasks begin.

When an active run exists, use the local gate checker before implementation:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard
```

Before claiming completion, use the local gate checker again:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard
```

Before claiming completion, use the completion gate:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion
```

## Skill Compatibility

Workflow skills may be used when they help satisfy the local spec, plan, gates, or verification requirements. They do not replace this repository's harness.

Use [harness/controls/skills.md](harness/controls/skills.md) to map workflow skills to local stages. If an external skill conflicts with project commands, guardrails, or user instructions, follow the local harness and ask when the conflict is material.

## Agent Workflow

1. Determine the initialization mode from `harness/context/initialization-notes.md`.
2. For greenfield work, read `project-brief.md`, then the active run's `workflow.md`, `design.md`, `spec.md`, and `plan.md`.
3. For brownfield work, read needed files under `harness/context/`, then existing project documentation/configuration, then the active run.
4. Read `harness/controls/lifecycle.md`, `gates.md`, and `skills.md`.
5. Load only the needed context files.
6. Check controls and guardrails before editing.
7. Confirm there are no unresolved blocking questions before editing application code.
8. Run the before-implementation gate when an active run exists.
9. Execute one small task at a time.
10. Run approved verification commands.
11. Record evidence in the run directory before claiming completion.
12. Create or update `review.md`.
13. Run the before-completion gate when an active run exists.
14. Update evaluation before handoff.
15. Review `Context Updates`, `execution-log.md`, `review.md`, and `evaluation.md` for harness gaps.
16. Update canonical harness files only when the user asked for harness maintenance, the active workflow explicitly allows it, or the update is a factual correction from repository evidence. Otherwise, list proposed harness updates for confirmation.

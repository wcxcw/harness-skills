---
name: context-budget
description: Decide which project harness context to load for a task and prevent bulk-reading long context files or completed run history.
---

# Context Budget

Use this skill when a project has multiple harness context files, long run history, or the current task risks loading more context than it needs.

## Gate Contract

- Owns selective context decisions before implementation and review.
- Records context choices in `workflow.md`, `spec.md`, `execution-log.md`, or `evaluation.md` when they affect the run.
- Keeps `harness/context/project-brief.md` as the short default orientation source, reuses it when already loaded in the same session, and treats other context files as task-triggered reads.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually no artifact; mention skipped/targeted context only when relevant | No review artifact gate |
| `standard` | Record non-default context reads in `workflow.md` or `execution-log.md` when they affect implementation | Supports `check_run.py` evidence and residual-risk tracking |
| `full` | Record context sources and skipped large files in `workflow.md` or `evaluation.md` | Required context rationale before broad implementation/review |

## Output

Use the smallest relevant artifact:

```text
harness/runs/YYYY-MM-DD-short-task-name/workflow.md
harness/runs/YYYY-MM-DD-short-task-name/execution-log.md
harness/runs/YYYY-MM-DD-short-task-name/evaluation.md
```

Suggested note:

```markdown
## Context Budget
- Default orientation: `harness/context/project-brief.md` read once or reused when already loaded
- Task-triggered read: `harness/context/coding-conventions.md` because frontend code changed
- Skipped: completed run history; not relevant to this objective
```

## Review Procedure

1. Start with `AGENTS.md`, `harness/context/project-brief.md`, `harness/controls/gates.md`, `harness/tools/commands.md`, and `harness/guardrails/boundaries.md` only when project orientation is missing, stale, or needed for the task.
2. Read the active run only when the request belongs to that run.
3. Before reading any extra `harness/context/*` file, state the task reason for reading it.
4. Prefer targeted search, headings, or small sections over whole-file reads for large context.
5. Treat completed runs as historical records; read them only when the user asks for history or the current task depends on that run.
6. Record skipped context as residual risk when not reading it could affect the decision.

## Context Defaults

- Safe default orientation source: `harness/context/project-brief.md`, if it remains a short project summary; reuse it within the same session when already loaded and not stale.
- Task-triggered: `coding-conventions.md`, `repo-map.md`, `architecture.md`, `dependency-notes.md`, and active run files.
- Historical: completed `harness/runs/*`; do not bulk-read during routine work.
- Large files: search first, then read targeted sections.

## Stop Conditions

- The task depends on project facts that are missing from the short brief and cannot be inferred safely.
- A required context file is too large and no targeted section/search strategy is available.
- Completed run history is necessary to understand user intent but no relevant run can be identified.
- Context sources conflict and the conflict changes implementation scope.

## Evidence Examples

```markdown
## Context Budget
- Read `harness/context/project-brief.md` and active `spec.md`.
- Read `harness/context/coding-conventions.md` because code quality review was required.
- Did not read completed runs; no historical dependency for this task.
```

## Anti-Patterns

- Reading every file under `harness/context/` at session start.
- Loading completed run directories to understand a new task.
- Treating a long `project-brief.md` as a safe default instead of asking to trim it.
- Skipping needed context and then presenting guesses as project facts.

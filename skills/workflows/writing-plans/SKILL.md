---
name: writing-plans
description: Turn an accepted `spec.md` into a scoped, ordered, verifiable `plan.md`.
---

# Writing Plans

Create `plan.md` from an accepted spec. This workflow replaces the old `task-planning` skill.

## Gate Contract

- Owns `plan.md` and the planning entry in `workflow.md`.
- `standard` and `full` tier runs require `plan.md` before `check_run.py --stage before-implementation` can pass.
- Do not proceed to implementation until the local before-implementation gate passes for the selected tier.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped; explain direct execution in `evaluation.md` | No planning artifact gate |
| `standard` | `plan.md` with `## Tasks` and `## Verification` | Required before `check_run.py --stage before-implementation` can pass |
| `full` | `plan.md` mapped from `design.md` and `spec.md` | Required before implementation and review |

## Output

Save the final plan to:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Update `workflow.md` with `writing-plans` under `## Skills Used`.

## Rules

- Plan from `spec.md`, not memory.
- Read `workflow.md`, `design.md` when present, `harness/controls/lifecycle.md`, `harness/controls/gates.md`, and relevant source files before planning.
- Do not plan coding tasks around unresolved blocking decisions.
- Split work into small tasks with dependencies, likely files, acceptance mapping, verification command, and evidence destination.
- Add checkpoints after risky tasks.
- Do not implement while planning.
- Prefer tasks that can be completed and verified independently. If a task cannot be verified, rewrite it.
- Put setup, schema, behavior, UI, docs, and tests in dependency order.

## Task Format

Use this shape under `## Tasks`:

```markdown
- [ ] Task N: [short imperative name]
  - Depends on: [task numbers or "None"]
  - Files: [likely files or directories]
  - Acceptance: [spec criterion IDs or text]
  - Verification: [exact command or manual check]
  - Evidence: append result to `execution-log.md`
```

## Self-Review

Before handoff, verify every acceptance criterion from `spec.md` maps to at least one task and one verification step. Remove vague tasks such as "polish", "integrate", or "finish" unless they name concrete files and evidence.

## Stop Conditions

- `spec.md` contains unresolved blockers.
- A task cannot name likely files, acceptance mapping, or verification.
- Required commands are unknown and cannot be found in `harness/tools/commands.md` or project docs.
- The plan depends on broad refactoring not accepted by the spec.

## Evidence Examples

```markdown
- [ ] Task 2: Add run gate validation
  - Depends on: Task 1
  - Files: `harness/scripts/check_run.py`, `tests/test_agent_harness_scaffold.py`
  - Acceptance: standard tier rejects missing `plan.md`
  - Verification: `python3 -m unittest tests/test_agent_harness_scaffold.py`
  - Evidence: append command result to `execution-log.md`
```

## Anti-Patterns

- Planning from memory instead of reading `spec.md`.
- Creating omnibus tasks like "implement backend" or "finish UI".
- Listing files without explaining why they are affected.
- Deferring verification to the end when a task can be checked immediately.

## Required Sections

```markdown
# Plan: [Name]

## Spec Source

## Overview

## Constraints and Risks

## Tasks

## Verification

## Parallelization Notes

## Open Questions
```

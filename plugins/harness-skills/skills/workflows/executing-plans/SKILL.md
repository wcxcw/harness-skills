---
name: executing-plans
description: Execute one approved `plan.md` task at a time while recording evidence in `execution-log.md`.
---

# Executing Plans

Use this skill after `check_run.py --stage before-implementation` passes.

## Gate Contract

- Owns `execution-log.md` during implementation.
- `xs`, `standard`, and `full` tier runs require completion evidence before `check_run.py --stage before-completion` can pass.
- Local gates decide continuation. If a plan step appears complete but evidence is missing, the step is not complete.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | `execution-log.md` with command or manual evidence | Required before `check_run.py --stage before-completion` can pass |
| `standard` | `execution-log.md` tied to `plan.md` tasks | Required before completion |
| `full` | `execution-log.md` plus later `review.md` | Required before review and final verification |

## Rules

- Read `AGENTS.md`, `harness/controls/`, `harness/guardrails/`, `spec.md`, and `plan.md`.
- Execute one plan task at a time in plan order unless the plan explicitly permits parallel work.
- Keep changes scoped to the task and spec.
- Run relevant approved commands from `harness/tools/commands.md`.
- Record changed files, commands, results, failures, and skipped checks in `execution-log.md`.
- Stop on blockers, failing required gates, missing files, or user decisions. Do not guess through a blocker.
- After each task, mark the task status in `plan.md` or record the checkpoint in `execution-log.md`.
- If implementation diverges from the plan, record the reason and update `plan.md` before continuing.
- If the user requests a correction to the same objective, continue the active run and append the new attempt, changed files, commands, and outcome to `execution-log.md` instead of creating a new run.

## Execution Log Format

Append entries like:

```markdown
## Task N: [name]

- Status: passed | blocked | failed | skipped
- Files changed:
  - `path/to/file`
- Commands:
  - `command`
- Result:
  - passed | failed | skipped, with important output summarized
- Notes:
  - [decision, blocker, or risk]
```

Update `workflow.md` with `executing-plans` under `## Skills Used`.

## Stop Conditions

- `check_run.py --stage before-implementation` fails for the selected tier.
- The current task is ambiguous, unverified, or no longer matches `spec.md`.
- A command fails and the cause is not understood.
- Required user approval, credentials, data, or environment is missing.

## Evidence Examples

```markdown
## Task 3: Enforce workflow adaptation tests

- Status: passed
- Files changed:
  - `tests/test_agent_harness_scaffold.py`
- Commands:
  - `python3 -m unittest tests/test_agent_harness_scaffold.py`
- Result:
  - passed, 7 tests
- Notes:
  - Gate coverage now checks local artifacts and `check_run.py`.
```

## Anti-Patterns

- Marking a task complete without a command result or manual check.
- Fixing unrelated code because it is nearby.
- Continuing after a failed command without diagnosis.
- Updating `plan.md` after the fact to match accidental implementation.
- Creating a new run for a follow-up correction that still belongs to the same user objective.

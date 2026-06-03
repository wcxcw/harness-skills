# AGENTS.md

This project uses an Agent Harness. Treat the files below as the shared source of truth for agent work.

## Read First

1. `harness/context/project-brief.md`
2. `harness/controls/gates.md`
3. `harness/tools/commands.md`
4. `harness/guardrails/boundaries.md`
5. The active run under `harness/runs/`, when one exists

## Core Rules

- Clarify unclear product, technical, or scope decisions before implementation.
- Use the smallest run tier that safely controls the task.
- For non-trivial work, create a run with `spec.md`, `plan.md`, `execution-log.md`, and `evaluation.md`.
- Record commands, manual checks, failures, skipped checks, and residual risk in the active run.
- Before implementation and completion, use `harness/scripts/check_run.py` when an active run exists.
- Do not invent project commands. Record unknown commands in `harness/tools/commands.md`.
- Keep changes scoped to the accepted spec and plan.
- Do not bypass `harness/guardrails/boundaries.md`.

## Run Tiers

```text
xs:       execution-log.md + evaluation.md
standard: workflow.md + spec.md + plan.md + execution-log.md + evaluation.md
full:     input.md + workflow.md + design.md + spec.md + plan.md + execution-log.md + review.md + evaluation.md
```

Use `full` only when product direction, architecture, data, security, CI, dependency, or review risk justifies it.

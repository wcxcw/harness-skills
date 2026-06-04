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
- Do not create a run for explicit, low-risk micro changes when no active run exists.
- A no-run micro change must be explicit, local to one surface or nearby file area, behavior-preserving, decision-free, easy to verify with one targeted check, and locally reversible.
- Examples: fix a typo, change one sentence of copy, change a named selector's font size from `18px` to `16px`, or adjust one spacing/color token.
- Not micro: "improve the homepage visuals", "adjust the typography hierarchy", cross-page changes, behavior changes, or anything requiring a design/product/technical decision.
- For micro changes, make the edit, run the smallest relevant check, and summarize the result in the response.
- When a run is warranted, use the smallest run tier that safely controls the task.
- Treat a run as one user objective, not one agent attempt.
- Continue the active run for follow-up corrections, test fixes, verification additions, and small adjustments to the same objective.
- Create a new run only when the objective changes, scope materially expands, the previous run is closed, or the user explicitly starts a new task.
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

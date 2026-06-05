# AGENTS.md

This project uses an Agent Harness. Treat the files below as the shared source of truth for agent work.

## Read First

1. `harness/context/project-brief.md`
2. `harness/controls/gates.md`
3. `harness/tools/commands.md`
4. `harness/guardrails/boundaries.md`
5. The active run under `harness/runs/`, only when the request belongs to an active run

## Context Loading

- Do not bulk-read `harness/context/*` or `harness/runs/*`.
- `harness/context/project-brief.md` is safe to read by default; when maintaining it, keep it to a short project summary and do not put detailed state, history, or long design content there.
- Read extra context files only after identifying why the current task needs them.
- Prefer targeted search or section reads over loading whole large files.
- Completed run directories are historical records; read them only when the user asks for history or the current task depends on that run.

## Core Rules

- Clarify unclear product, technical, or scope decisions before implementation.
- Run eligibility, tiers, and boundaries are defined in `harness/controls/gates.md`; use that file as the authority.
- If gates classify the request as a no-run micro change, edit directly, run the smallest relevant check, and summarize the result.
- If a run is warranted, use the smallest safe tier and keep one active run per user objective; append same-objective follow-ups to that run.
- For non-trivial work, create a run with `spec.md`, `plan.md`, `execution-log.md`, and `evaluation.md`.
- For application code changes, run code-quality review before final verification; use frontend/backend quality review when the changed surface applies.
- Record commands, manual checks, failures, skipped checks, and residual risk in the active run.
- Before implementation and completion, use `harness/scripts/check_run.py` when an active run exists.
- Do not invent project commands. Record unknown commands in `harness/tools/commands.md`.
- Keep changes scoped to the accepted spec and plan.
- Do not bypass `harness/guardrails/boundaries.md`.

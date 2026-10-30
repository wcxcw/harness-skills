# AGENTS.md

This project uses an Agent Harness. Treat the files below as the shared source of truth for agent work.

## Read First

Read or reuse these when orienting to the project or when the current task needs fresh harness context:

1. `harness/context/project-brief.md`
2. `harness/controls/gates.md`
3. `harness/tools/commands.md`
4. `harness/guardrails/boundaries.md`
5. The active run under `harness/runs/`, only when the request belongs to an active run

## Context Loading

- Do not bulk-read `harness/context/*` or `harness/runs/*`.
- `harness/context/project-brief.md` is safe to read by default; when maintaining it, keep it to a short project summary and do not put detailed state, history, or long design content there.
- Within the same session, reuse an already-loaded `project-brief.md` unless project facts changed, context was compacted, or the task needs reorientation.
- Read extra context files only after identifying why the current task needs them.
- Prefer targeted search or section reads over loading whole large files.
- Completed run directories are historical records; read them only when the user asks for history or the current task depends on that run.

## Core Rules

- Clarify unclear product, technical, or scope decisions before implementation.
- When the objective or material decisions are unclear and no run exists, invite the user to explicitly invoke `$grilling` before creating a run. Grilling stays conversational and creates no files; after confirmation, record the shared understanding directly in `spec.md`.
- Run eligibility, tiers, and boundaries are defined in `harness/controls/gates.md`; use that file as the authority.
- If gates classify the request as a no-run micro change, edit directly, run the smallest relevant check, and summarize the result.
- If a run is warranted, use the smallest safe tier and keep one active run per user objective; append same-objective follow-ups to that run.
- Bind a created or explicitly resumed run to the current session with `check_run.py <run> --tier <tier> --set-phase active`; never infer it from the most recently modified run directory.
- Create artifacts required by the selected tier: `xs` needs `execution-log.md` and `evaluation.md`; `standard` and `full` also require `workflow.md`, `spec.md`, and `plan.md`.
- For application code changes, run code-quality review before final verification; use frontend/backend quality review when applicable, unless the task is a no-run micro change or the skip reason is recorded as allowed by the gates.
- Record commands, manual checks, failures, skipped checks, and residual risk in the active run.
- Before implementation and completion, use `harness/scripts/check_run.py` when an active run exists.
- Only after final artifacts and the explicit completion gate pass, set the run phase to `verifying`; the session-scoped Stop hook closes it after a fresh recheck.
- Do not invent project commands. Record unknown commands in `harness/tools/commands.md`.
- Keep changes within the user's objective and any spec and plan required by the selected tier.
- Do not bypass `harness/guardrails/boundaries.md`.

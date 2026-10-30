---
name: workflows
description: Route closed-loop Agent Harness work through pre-run grilling and run-level skills such as writing-specs, writing-plans, executing-plans, code quality review, verification, and finishing-run.
---

# Workflows

Use this skill as the workflow layer for the full closed-loop harness. It routes work to the specific workflow files in this directory while keeping Harness Engineering as the control system.

## Workflow Order

0. `grilling/SKILL.md` before creating a run, only when the user explicitly invokes it
1. `writing-specs/SKILL.md` after the user confirms shared understanding or supplies an already-clear request
2. `writing-plans/SKILL.md`
3. `context-budget/SKILL.md` when project context or run history could become large
4. `executing-plans/SKILL.md`
5. Apply `test-driven-development/SKILL.md` during execution when automated tests fit the task
6. Apply `systematic-debugging/SKILL.md` during execution for bugfixes
7. `requesting-code-review/SKILL.md`
8. `code-reviewer/SKILL.md` for a focused code review when applicable
9. `code-quality-review/SKILL.md` for application code changes
10. `frontend-quality-review/SKILL.md` for frontend/UI/browser changes
11. `backend-quality-review/SKILL.md` for backend/API/service changes
12. `receiving-code-review/SKILL.md` when review feedback requires fixes
13. `finishing-run/SKILL.md` creates an initial `evaluation.md` after implementation and review
14. `verification-before-completion/SKILL.md` verifies the evidence and runs the completion gate; `finishing-run` finalizes the evaluation and lifecycle afterward

## Harness Contract

- For `standard` and `full`, record workflow usage in `workflow.md`; `xs` does not require it.
- Keep `grilling` outside the run: it creates no artifacts and is not recorded as a run workflow skill.
- Keep local gates in `harness/controls/gates.md` authoritative.
- Use `harness/controls/gates.md` and the selected tier to decide which artifact is required next. Consult `harness/controls/lifecycle.md` only when present.
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier xs|standard|full` before implementation when the selected tier requires it.
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier xs|standard|full` before claiming completion.
- For application code changes, run the appropriate quality review workflow before final verification unless the task is a no-run micro change or the skip reason is recorded.
- Do not bypass `check_run.py` because another workflow says to continue.
- The checker verifies its documented structural checks, not whether evidence is true or behavior is correct; assess those from actual results.

## Optional Advanced Modes

These modes can improve throughput on complex runs, but they are not required Harness stages:

- Use an isolated worktree when the task is risky, long-running, or may conflict with existing user changes.
- Use subagents for independent implementation tasks when the platform supports them and the plan is specific enough to split safely.
- Dispatch parallel agents only for independent research, review, or implementation units with explicit artifact handoff.

All advanced modes must still write to the local run artifacts: `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, and `evaluation.md` as required by the selected tier.

## Attribution

These workflows are adapted to this repository's Agent Harness artifacts and gates. Third-party attribution lives in `NOTICE.md`.

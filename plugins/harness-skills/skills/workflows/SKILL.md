---
name: workflows
description: Route closed-loop Agent Harness work through workflow skills such as brainstorming, writing-specs, writing-plans, executing-plans, code quality review, verification, and finishing-run.
---

# Workflows

Use this skill as the workflow layer for the full closed-loop harness. It routes work to the specific workflow files in this directory while keeping Harness Engineering as the control system.

## Workflow Order

1. `brainstorming/SKILL.md`
2. `writing-specs/SKILL.md`
3. `writing-plans/SKILL.md`
4. `context-budget/SKILL.md` when project context or run history could become large
5. `executing-plans/SKILL.md`
6. `test-driven-development/SKILL.md` when automated tests fit the task
7. `systematic-debugging/SKILL.md` for bugfixes
8. `requesting-code-review/SKILL.md`
9. `code-reviewer/SKILL.md` as the dedicated reviewer role when subagents are available
10. `code-quality-review/SKILL.md` for application code changes
11. `frontend-quality-review/SKILL.md` for frontend/UI/browser changes
12. `backend-quality-review/SKILL.md` for backend/API/service changes
13. `receiving-code-review/SKILL.md` when review feedback requires fixes
14. `verification-before-completion/SKILL.md`
15. `finishing-run/SKILL.md`

## Harness Contract

- Record workflow usage in `workflow.md`.
- Keep local gates in `harness/controls/gates.md` authoritative.
- Use `harness/controls/lifecycle.md` to decide which artifact is required next.
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier xs|standard|full` before implementation when the selected tier requires it.
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier xs|standard|full` before claiming completion.
- For application code changes, run the appropriate quality review workflow before final verification unless the task is a no-run micro change or the skip reason is recorded.
- Do not bypass `check_run.py` because another workflow says to continue.

## Optional Advanced Modes

These modes can improve throughput on complex runs, but they are not required Harness stages:

- Use an isolated worktree when the task is risky, long-running, or may conflict with existing user changes.
- Use subagents for independent implementation tasks when the platform supports them and the plan is specific enough to split safely.
- Dispatch parallel agents only for independent research, review, or implementation units with explicit artifact handoff.

All advanced modes must still write to the local run artifacts: `workflow.md`, `design.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, and `evaluation.md` as required by the selected tier.

## Attribution

These workflows are adapted to this repository's Agent Harness artifacts and gates. Third-party attribution lives in `NOTICE.md`.

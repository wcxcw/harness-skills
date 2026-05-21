---
name: task-planning
description: Create a run-level implementation plan from an accepted spec. Use when `spec.md` is ready and work needs to be broken into ordered, scoped, verifiable tasks before implementation.
---

# Task Planning

Create `plan.md` from an accepted `spec.md`. The plan defines implementation order, task scope, dependencies, likely files, verification, and required evidence.

This skill only owns `plan.md`. Do not rewrite the spec and do not implement code while planning.

## Harness Output

Save the final plan to the active harness run:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

If no active run exists, create or ask for the intended run directory under `harness/runs/`. Do not create a separate documentation directory.

## Planning Principles

- Plan from the accepted spec, not from memory.
- Stay read-only while planning.
- Do not plan coding tasks around unresolved blocking decisions.
- Keep each task small enough for one focused implementation pass.
- Make dependencies and likely files explicit.
- Define verification and required evidence for every task.
- Prefer the smallest implementation path that satisfies the spec.
- Leave the system in a working state after each task or checkpoint.

## Default Flow

1. Read the active `spec.md`, then only the harness context and source files needed to understand scope.
2. Identify dependencies, risk, and ordering constraints.
3. If the spec has unresolved technology, architecture, data, service, deployment, or user-flow decisions, make the first task a non-coding decision task and do not add implementation tasks that depend on it.
4. Split work into small tasks. Prefer vertical slices when they reduce integration risk, but do not force a product-style phase structure.
5. Assign likely files or modules for each task.
6. Add verification and evidence required for each task.
7. Add checkpoints after risky tasks or after every 2-3 tasks.
8. Ask the user to confirm the plan before implementation when the plan changes architecture, data, dependencies, or user-visible scope.

## Task Sizing

| Size | Use For | Guidance |
| --- | --- | --- |
| XS | One function, config, copy, or small test change | Safe as a single task. |
| S | One component, endpoint, command, or focused behavior | Preferred agent task size. |
| M | One complete behavior slice touching a few files | Acceptable with clear verification. |
| L | Multiple subsystems or broad refactor | Split before implementation. |

Break a task down further when it touches unrelated subsystems, cannot be verified independently, has more than 3 acceptance checks, or uses "and" in the title.

## Plan Template

```markdown
# Plan: [Project/Feature/Fix Name]

## Spec Source
- Run: [harness/runs/YYYY-MM-DD-short-task-name]
- Spec: [spec.md]

## Overview
[Short implementation approach. Do not restate the whole spec.]

## Constraints and Risks
- [Constraint or risk that affects ordering.]

## Tasks

### Task 1: [Short action title]
**Goal:** [What this task accomplishes.]

**Scope:**
- [Included work.]
- [Excluded work if needed.]

**Likely files:**
- `path/to/file`

**Dependencies:** None | Task [N]

**Acceptance:**
- [ ] [Task-level acceptance check.]

**Verification:**
- [ ] [Command or manual check.]

**Evidence required:** [Command output, test result, manual check, or artifact.]

### Checkpoint: [Name]
- [ ] [Verification or review checkpoint.]

## Parallelization Notes
- Safe to parallelize: [independent tasks or "None"]
- Must be sequential: [dependency chain or "None"]

## Open Questions
- [Question that blocks implementation or "None"]
```

## Implementation Gate

Do not start coding from a plan that contains unresolved blocking questions. If a decision is unresolved, the plan must begin with a non-coding task to resolve it, and dependent implementation tasks must wait.

## Quality Bar

Before implementation starts:

- [ ] Every task maps back to the accepted spec.
- [ ] Every task has clear scope.
- [ ] Every task has likely files or modules.
- [ ] Every task has acceptance criteria.
- [ ] Every task has verification and required evidence.
- [ ] Dependencies are ordered correctly.
- [ ] Large tasks are split or explicitly marked as requiring user approval.
- [ ] Open questions are resolved or carried forward.
- [ ] No coding task depends on an unresolved technology, architecture, data, service, deployment, or user-flow decision.

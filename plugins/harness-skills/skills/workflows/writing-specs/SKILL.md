---
name: writing-specs
description: Create a run-level executable `spec.md` with scope, decisions, acceptance criteria, verification, and blocking questions.
---

# Writing Specs

Create the task contract before implementation. This workflow replaces the old `spec-driven-development` skill and keeps the local harness decision gate authoritative.

## Gate Contract

- Owns `spec.md` and the spec entry in `workflow.md`.
- `standard` and `full` tier runs require `spec.md` before `check_run.py --stage before-implementation` can pass.
- Local gates decide continuation; the spec must not contain unresolved blocking decisions unless the next step is explicitly a decision task.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Only use when the task has hidden product or technical risk | Blocking markers are still checked if `spec.md` exists |
| `standard` | `spec.md` plus `workflow.md` skill record | Required before `check_run.py --stage before-implementation` can pass |
| `full` | `spec.md` after `design.md` | Required before `plan.md` and implementation |

## Output

Save the final spec to:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

Update `workflow.md` with `writing-specs` under `## Skills Used`.

## Rules

- Read `design.md` when present.
- Read `workflow.md`, `harness/controls/lifecycle.md`, and `harness/controls/gates.md` before setting the run tier.
- Define objective, scope, non-goals, assumptions, acceptance criteria, verification, and evidence.
- Mark unresolved product or technical decisions as `Needs decision`.
- Do not convert unresolved blocking decisions into assumptions to keep moving.
- Do not produce an implementation plan. Planning belongs to `writing-plans`.
- Write acceptance criteria as observable outcomes that can be checked by command output, artifact inspection, or explicit manual verification.

## Required Sections

```markdown
# Spec: [Name]

## Objective

## Target User

## In Scope

## Out of Scope

## Assumptions

## Product Decisions

## Technical Decisions

## Acceptance Criteria

## Verification

## Evidence Required

## Constraints

## Context Updates

## Open Questions
```

Before handing off, `Product Decisions`, `Technical Decisions`, and `Open Questions` must not contain unresolved blockers unless the next plan task is explicitly a non-coding decision task.

## Stop Conditions

- `Objective`, `In Scope`, `Out of Scope`, acceptance, or verification cannot be stated concretely.
- Any required decision is still `Needs decision` and the next task is not a decision task.
- Acceptance criteria cannot be checked by command, artifact inspection, or explicit manual verification.
- The user is asking to implement before scope is stable.

## Evidence Examples

```markdown
## Acceptance Criteria
- [ ] `check_run.py --stage before-implementation --tier standard` passes for a complete run.

## Verification
- [ ] Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard`.
```

## Anti-Patterns

- Replacing unknowns with assumptions to keep moving.
- Mixing implementation tasks into `spec.md`.
- Writing acceptance criteria that say "works correctly" without observable checks.
- Omitting out-of-scope items because they feel obvious.

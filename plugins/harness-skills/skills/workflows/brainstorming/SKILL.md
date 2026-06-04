---
name: brainstorming
description: Shape a raw idea, vague feature, or early product direction into a harness-ready `design.md` before spec writing.
---

# Brainstorming

Use this skill when the user starts with an unclear idea, product direction, or feature concept. The output is a compact design artifact that can feed `writing-specs`.

This workflow is adapted for the local Agent Harness. It replaces the old `idea-refine` skill.

## Gate Contract

- Owns `design.md` and the intake entry in `workflow.md`.
- For `full` tier runs, `design.md` is required before `check_run.py --stage before-implementation` can pass.
- For `standard` or `xs` runs, record why intake was skipped or compressed in `workflow.md` or `evaluation.md`.
- Local gates decide continuation; brainstorming never authorizes implementation by itself.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Intake note in `evaluation.md` when relevant | No pre-implementation artifact gate |
| `standard` | `workflow.md` records whether intake was used or skipped | Supports later `spec.md` and `plan.md` checks |
| `full` | `design.md` plus `workflow.md` | Required before `check_run.py --stage before-implementation` can pass |

## Output

Save the result in the active run:

```text
harness/runs/YYYY-MM-DD-short-task-name/design.md
```

Also update `workflow.md` with:

```markdown
## Skills Used
- brainstorming

## Gates
- Intake direction confirmed: yes | no
```

## Flow

1. Inspect the repository context first: README, AGENTS, current harness controls, existing specs, and relevant source structure.
2. Restate the idea as a concrete problem and name the target user or operator.
3. Ask one focused question at a time when target user, product shape, content/data, stack, risk, or success criteria are unclear. Keep the total to the smallest useful set.
4. Propose 2-3 viable approaches when the solution space is still open, then recommend one direction with tradeoffs.
5. Stress-test the recommended direction against constraints, likely failure modes, data availability, and maintenance cost.
6. Define the smallest MVP that validates the core assumption.
7. Record explicit non-goals and decisions that must not be reopened during implementation.
8. Stop before spec if blocking decisions remain.

## Self-Review

Before handing off to `writing-specs`, check that `design.md` has no placeholders, vague owners, hidden dependencies, or unresolved decisions disguised as assumptions. If a decision is missing, mark it as `Needs decision` and keep the run from advancing.

## Stop Conditions

- Target user, product shape, data/content source, or success criteria are unknown.
- The user has not chosen among materially different approaches.
- A decision is still marked `Needs decision`.
- The requested scope cannot fit the selected tier without hiding risk.

## Evidence Examples

```markdown
## Gates
- Intake direction confirmed: yes
- Recommended approach accepted: yes
- Open decisions: None
```

```markdown
## Gates
- Intake direction confirmed: no
- Blocker: content source is `Needs decision`
```

## Anti-Patterns

- Starting `spec.md` while the design still contains placeholder decisions.
- Asking a long questionnaire instead of one focused question at a time.
- Presenting many options without a recommendation.
- Treating the first idea as approved without checking constraints and failure modes.

## Design Template

```markdown
# Design: [Name]

## Problem
[What problem are we solving?]

## Target User
[Specific user or buyer.]

## Success Criteria
- [Testable outcome.]

## Content or Data Scope
- [Sources, inputs, outputs, update cadence, or "Needs decision".]

## Core Experience
- [Primary workflow, pages, or system behavior.]

## Recommended Direction
[Chosen direction and why.]

## MVP
[Smallest version worth building.]

## Non-Goals
- [Explicitly out of scope.]

## Open Questions
- [Question or "None".]
```

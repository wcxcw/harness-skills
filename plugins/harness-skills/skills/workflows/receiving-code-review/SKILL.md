---
name: receiving-code-review
description: Process code review feedback rigorously, verify each finding against the codebase, apply valid fixes one at a time, and record resolution in the active run.
---

# Receiving Code Review

Use this skill when the user, another reviewer, or a review workflow provides feedback on completed changes.

## Gate Contract

- Owns review feedback resolution in `review.md`, `execution-log.md`, and `evaluation.md`.
- Same-objective review fixes stay in the current active run; do not create a new run for review-driven corrections.
- Review suggestions must be verified against the codebase before implementation, especially when they are broad, ambiguous, or external.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Append fix evidence to `execution-log.md` and risk note to `evaluation.md` | Required before completion when feedback affects acceptance |
| `standard` | Update `review.md` Resolution plus `execution-log.md` verification | Required before completion when review findings exist |
| `full` | Resolve every `review.md` finding or record explicit accepted residual risk | Required before `check_run.py --stage before-completion` can pass |

## Output

Update the active run:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
harness/runs/YYYY-MM-DD-short-task-name/execution-log.md
harness/runs/YYYY-MM-DD-short-task-name/evaluation.md
```

## Review Procedure

1. Read the full feedback before editing.
2. Restate unclear items as technical requirements or ask the user for clarification.
3. Verify each item against the codebase, existing tests, accepted spec, and local conventions.
4. Reject or defer incorrect suggestions only with technical reasoning and recorded residual risk when needed.
5. Fix valid findings one at a time, from blocking issues to simple fixes to complex refactors.
6. Run the smallest relevant check after each meaningful fix or batch of tightly related fixes.
7. Update `review.md` with resolution status and append verification evidence to `execution-log.md`.
8. Re-run `check_run.py --stage before-completion` when the active run exists and the checker is available.

## Response Pattern

- Prefer technical acknowledgement or direct action over performative agreement.
- Ask before implementing ambiguous multi-item feedback.
- Push back when a suggestion breaks accepted scope, project conventions, compatibility, or user decisions.
- Keep review fixes within the same run unless the user changes the objective or expands scope materially.

## Stop Conditions

- Feedback items are unclear enough that implementation could target the wrong change.
- A suggestion conflicts with the accepted spec, user decision, or project constraint.
- A fix would expand scope beyond the active run.
- Required verification cannot be run and no substitute evidence is recorded.

## Evidence Examples

```markdown
## Resolution
- Finding: Root component owns API and modal state.
- Status: fixed
- Change: extracted `useItems` and `ItemList`.
- Verification: `npm run build` passed; mobile browser check passed.
```

## Anti-Patterns

- Creating a new run for every review fix to the same objective.
- Blindly implementing external feedback without checking local code.
- Partially implementing a multi-item review when some items are unclear.
- Marking findings fixed without verification evidence.

---
name: frontend-quality-review
description: Review frontend changes for component boundaries, state/data separation, accessibility, responsive behavior, and browser verification.
---

# Frontend Quality Review

Use this skill for UI, frontend, browser, or client-side application changes after implementation and before completion.

## Gate Contract

- Owns a frontend-specific review contribution; `requesting-code-review` merges it into the complete `review.md`.
- Composes with `code-quality-review`; do not duplicate generic findings when a frontend-specific finding is clearer.
- Requires browser or DOM verification when the changed UI can be exercised locally.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped for one explicit style token or copy edit; record the targeted check in `execution-log.md` | No review artifact gate |
| `standard` | Frontend review notes in `review.md` for feature UI, state, routing, or multi-file frontend work | Important findings block completion until resolved or accepted |
| `full` | Frontend review plus browser evidence and resolution in `review.md`/`execution-log.md` | Required before `check_run.py --stage before-completion` can pass |

## Output

Return a contribution for:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

Use a third-level dimension heading for placement under the canonical
`## Findings` section. Record browser commands and manual evidence in
`execution-log.md`, not as another top-level review section.

```markdown
### Frontend Quality Review
- Severity: Critical | Important | Minor
- Location:
- Issue:
- Required action:
- Proposed resolution: pending
```

## Review Procedure

1. Identify changed frontend files and the user-facing workflow they affect.
2. Check root/page components first: they should orchestrate layout and composition, not own all API calls, state transitions, rendering branches, and business logic.
3. Split meaningful UI parts into components, stateful logic into composables/hooks/stores, and server calls into existing API/data helpers when the project has those patterns.
4. Check responsive behavior, text overflow, loading/error/empty states, keyboard and accessibility basics, and visual regressions.
5. Run the smallest relevant frontend checks from `harness/tools/commands.md`, such as lint, typecheck, build, tests, or browser verification.
6. Return findings to the coordinator; record browser evidence and skipped checks in `execution-log.md`, and merge accepted residual risk into the canonical `## Residual Risk` section.

## Quality Baseline

- `App.vue`, root React components, and route shells should remain composition shells unless the task is a tiny demo or the project already uses a single-file pattern.
- Do not mix view markup, server requests, persistence, state machines, formatting utilities, and business rules in one component when a local split is available.
- Components should expose clear props/events and avoid hidden global coupling.
- UI work should include expected states: default, loading, empty, error, disabled, focused/hovered when relevant.
- Browser-visible changes should be verified in a real browser or explicitly recorded as skipped with a reason.

## Stop Conditions

- The app cannot be built or opened and no substitute verification is recorded.
- A root/page component accumulates multiple unrelated responsibilities without an accepted reason.
- Browser evidence is required but missing.
- Important accessibility, responsive, or state-handling findings are unresolved.

## Evidence Examples

```markdown
### Frontend Quality Review
- Severity: Important
- Location: `src/App.vue:42`
- Issue: API loading, filtering state, and card rendering are all implemented in the root shell.
- Required action: move data access into `useItems` and extract the list/card components.
- Proposed resolution: fixed

Execution evidence:
- Command: npm run build
- Manual: checked 390px and 1440px viewports
```

## Anti-Patterns

- Shipping UI after only reading code when a local browser check is possible.
- Treating `App.vue` or a route file as the default place for all feature logic.
- Ignoring mobile overflow, loading states, or error states because the happy path works.
- Adding competing top-level review sections instead of returning a dimension contribution.
- Adding decorative UI that conflicts with the project's established design system.

# Coding Conventions

Record project-specific conventions that agents must follow.

## Style

- [Naming, formatting, component, or module convention]
- Prefer existing project structure and local helper APIs over new patterns.
- Keep root app files, route shells, controllers, and services focused on orchestration.
- Split code when UI, state, data access, business rules, and formatting start sharing one large file.

## Frontend Structure

- Keep root components such as `App.vue` or top-level React app files as composition shells unless the project intentionally uses a single-file demo pattern.
- Move stateful reusable logic into composables/hooks/stores when the framework supports it.
- Move server calls into existing API/data helpers instead of embedding them in view components.
- Verify browser-visible changes in a real browser when local execution is available.

## Backend Structure

- Keep handlers/controllers thin when the project has service or data layers.
- Validate input at trust boundaries and preserve authorization, schema, and compatibility assumptions.
- Add logs for important external calls, state changes, background work, and exceptional paths when the project has logging facilities.

## Error Handling

- [Project-specific expectation]
- Do not swallow errors or replace useful diagnostics with vague success/failure states.
- Record skipped error-path verification as residual risk.

## Testing

- [Where tests live and what style they use]

## Comments

- Add comments for non-obvious business rules, edge cases, invariants, tradeoffs, and integration constraints.
- Do not add comments that only restate obvious syntax.

## Review Expectations

- Keep changes scoped to the active spec.
- Prefer existing patterns over new abstractions.
- Add comments only where they clarify non-obvious logic.
- Code quality findings are not automatically "style"; treat maintainability, logging, error handling, and testability gaps as review findings when they affect future work.

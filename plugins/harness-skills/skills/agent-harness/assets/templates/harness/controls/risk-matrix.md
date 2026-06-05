# Risk Matrix

Use this matrix to choose the smallest safe tier, review depth, and verification scope.

## Risk Factors

| Risk | Examples | Minimum response |
| --- | --- | --- |
| Data loss | delete/update flows, migrations, persistence changes | `full` run, backend quality review, explicit rollback notes |
| Security/auth | authentication, authorization, secrets, permissions | `full` run, security-focused review, tests or manual evidence |
| API/data contract | request/response shape, schema, external integration | `standard` or `full`, contract verification |
| Architecture | module boundaries, shared state, dependency direction | `full` when new direction is introduced |
| Frontend UX | navigation, core flow, accessibility, responsive layout | frontend quality review and browser evidence |
| Observability | backend side effects, background jobs, external calls | backend quality review and logging check |
| Dependency/CI | package changes, toolchain, build/test pipeline | `standard` or `full`, build and rollback evidence |
| Context size | large context files, long run history, ambiguous project facts | context-budget before implementation |

## Tier Rules

- Use no-run only when every micro-change criterion in `gates.md` is met.
- Use `xs` for low-risk changes that still need evidence.
- Use `standard` for normal feature work, contained bugfixes, and multi-file changes.
- Use `full` when any high-risk factor affects data, security, architecture, product direction, CI, or broad UX behavior.

## Review Rules

- Application code changes need code-quality review unless explicitly skipped with a reason.
- Frontend changes use frontend quality review when UI, state, routing, accessibility, or browser behavior changes.
- Backend/API/service changes use backend quality review when data, errors, logs, side effects, or external calls change.
- Critical and Important review findings block completion until fixed or accepted by the user as residual risk.

## Evidence Rules

- Riskier work needs stronger evidence: lint/build/test plus targeted manual or browser/API verification.
- Skipped checks must explain why the check could not run and what substitute evidence was used.
- If risk cannot be classified, stop and ask or record the unknown as a blocking decision.

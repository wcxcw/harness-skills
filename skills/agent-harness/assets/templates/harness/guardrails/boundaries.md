# Boundaries

## Always

- Work from the active spec and plan.
- Read relevant files before editing.
- Keep changes scoped to the requested behavior.
- Record commands and verification results.
- Prefer the simplest change that satisfies the spec.
- Keep useful existing patterns instead of inventing new ones.

## Ask First

- Scope expands beyond the active spec.
- Requirements conflict with existing architecture.
- Verification requires external credentials or production systems.
- A change would introduce a new dependency, framework, service, or broad abstraction.

## Never

- Invent unverified commands.
- Hide failing tests or skipped checks.
- Modify generated, vendor, or lock files unless needed and understood.
- Add speculative abstractions for unrequested future needs.
- Treat "code changed" as completion without verification evidence.

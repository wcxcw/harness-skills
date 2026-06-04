# Boundaries

## Always

- Work from the active spec and plan.
- Read relevant files before editing.
- Keep changes scoped to the requested behavior.
- Record commands and verification results.
- Prefer the simplest change that satisfies the spec.
- Keep useful existing patterns instead of inventing new ones.
- Treat canonical harness files as repository-owned source of truth.

## Ask First

- Scope expands beyond the active spec.
- Requirements conflict with existing architecture.
- Verification requires external credentials or production systems.
- A change would introduce a new dependency, framework, service, or broad abstraction.
- A normal feature or bugfix run wants to modify `AGENTS.md` or canonical `harness/` files instead of proposing the update in `evaluation.md`.

## Never

- Invent unverified commands.
- Hide failing tests or skipped checks.
- Modify generated, vendor, or lock files unless needed and understood.
- Add speculative abstractions for unrequested future needs.
- Treat "code changed" as completion without verification evidence.
- Replace the shared repository harness with personal local notes.

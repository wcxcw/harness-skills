# Rollback

Define recovery steps when a run fails or produces risky changes.

## Before Risky Changes

- Identify files likely to change.
- Confirm current git status when working in a repository.

## Recovery

- Prefer small follow-up patches over broad reverts.
- Do not revert user changes without explicit approval.
- Document failed commands and suspected cause in `execution-log.md`.

## Handoff

- State what changed.
- State what verification passed or failed.
- State residual risks and recommended next action.

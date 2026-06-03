# Permissions

Define what agents can do without approval and what requires human confirmation.

## Allowed Without Approval

- Read project files.
- Edit files in scope for the active spec.
- Run documented local verification commands.

## Ask First

- Add or remove dependencies.
- Change database schema or migrations.
- Change CI/CD configuration.
- Delete tests or large code paths.
- Perform destructive filesystem or git operations.

## Never

- Commit secrets.
- Exfiltrate private data.
- Remove failing tests to make verification pass.
- Rewrite unrelated modules.

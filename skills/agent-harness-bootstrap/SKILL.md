---
name: agent-harness-bootstrap
description: Initialize and operate a project-level Agent Harness for software engineering work. Use when the user wants to create or update Agents.md, scaffold a harness/ directory, define spec/context/tools/guardrails/evals templates, create run records, or combine bundled skills such as spec-driven-development, planning-and-task-breakdown, and browser-testing-with-devtools into a repeatable Harness Engineering workflow.
---

# Agent Harness Bootstrap

## Overview

Use this skill to bootstrap and operate an Agent Harness: a controlled loop that tells agents what to do, what not to do, which context to load, which tools to use, how to record work, and how to evaluate completion.

This is an orchestration skill. Do not duplicate the full workflows of related skills. Use this skill to create the project harness and route work to the right supporting skill when needed.

## Workflow

### 1. Discover

Inspect the target project before writing harness files:

- Source layout and app type
- Package manager and runtime
- Build, test, lint, dev, and verification commands
- Existing documentation, CI, tests, and conventions
- Whether the project has browser-facing behavior

Prefer project-specific facts over generic templates. If a command is unknown, leave a clear placeholder in `harness/tools/commands.md`.

### 2. Bootstrap

Create or update these files from `assets/templates/`:

```text
Agents.md
harness/
├── specs/
├── context/
├── tools/
├── guardrails/
├── evals/
└── runs/
```

Use `scripts/init_harness.py` for deterministic scaffolding when creating the structure from scratch.

### 3. Specify

For non-trivial tasks, use `spec-driven-development`. Save the resulting task contract in the active run directory:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

The spec must define goal, scope, non-goals, acceptance criteria, verification, and open questions.

### 4. Plan

After the spec is clear, use `planning-and-task-breakdown`. Save the implementation plan in:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Tasks should be small, ordered by dependency, and include verification steps.

### 5. Execute

Implement against the active run only:

- Read `Agents.md`
- Read the active run's `spec.md` and `plan.md`
- Load only the needed files under `harness/context/`
- Check `harness/guardrails/` before edits
- Keep code changes scoped to the current spec

### 6. Verify

Run commands from `harness/tools/commands.md` and record results in `execution-log.md`.

For browser projects, use `browser-testing-with-devtools` after implementation to inspect the app in a real browser, including console errors, network failures, layout issues, and relevant screenshots.

### 7. Record

Each task run should use this structure:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Record changed files, commands run, verification results, unresolved risks, and whether each acceptance criterion passed.

### 8. Improve

After each run, update the harness if the run exposed a gap:

- Missing or stale context
- Unclear commands
- Weak guardrails
- Ambiguous evaluation criteria
- Repeated agent mistakes

Update harness files, not unrelated application code, during this improvement phase.

## Related Skills

Read `references/related-skills.md` when deciding how this skill composes with existing skills. In short:

- Use bundled `spec-driven-development` for the Spec layer.
- Use bundled `planning-and-task-breakdown` for the Plan and Tasks layer.
- Use bundled `browser-testing-with-devtools` for browser verification when the runtime tools are available.

## Boundaries

- Do not install this skill globally unless the user asks.
- Do not create a large agent platform before the project-level harness loop works.
- Do not invent commands that were not found or confirmed.
- Ask before adding dependencies, changing schemas, altering CI, or deleting tests.
- Never remove failing tests just to pass verification.

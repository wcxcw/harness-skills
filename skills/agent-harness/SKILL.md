---
name: agent-harness
description: Initialize and operate a project-level Agent Harness for software engineering work. Use when the user wants to create or update AGENTS.md, scaffold a harness/ directory, define spec/context/tools/guardrails/evals templates, create run records, or combine bundled skills such as idea-refine, spec-driven-development, and task-planning into a repeatable Harness Engineering workflow.
---

# Agent Harness

## Overview

Use this skill to bootstrap and operate an Agent Harness: a controlled loop that tells agents what to do, what not to do, which context to load, which tools to use, how to record work, and how to evaluate completion.

This is an orchestration skill. Do not duplicate the full workflows of related skills. Use this skill to create the project harness and route work to the right supporting skill when needed.

## Operating Principles

- Clarify before coding: turn vague requests into explicit goals, constraints, and success criteria.
- Spec before implementation: non-trivial work needs a run-level spec before code changes.
- Plan into small verifiable tasks: each task should have scope, likely files, dependencies, and verification.
- Evidence before completion: do not claim completion without commands, checks, or a documented reason verification was skipped.
- Keep scope small: prefer the simplest change that satisfies the spec; avoid unrelated refactors or speculative abstractions.
- Improve the harness from evidence: repeated failures, missing commands, stale context, or weak guardrails should feed back into canonical harness files.

## Workflow

### 1. Choose Initialization Mode

Choose one mode before scaffolding or updating harness files:

- `greenfield`: Use when the project is empty, has no source or manifest files, or the user describes a new project from a short idea.
- `brownfield`: Use when the project already has source code, manifests, tests, CI, README, or other implementation history.
- `existing-harness`: Use when `AGENTS.md` or `harness/` already exists.

For `existing-harness`, preserve existing harness content by default. Add missing files, refresh stale placeholders, and propose larger rewrites only when the user asks.

### 2. Discover

Inspect the target project before writing harness files:

- Source layout and app type
- Package manager and runtime
- Build, test, lint, dev, and verification commands
- Existing documentation, CI, tests, and conventions

For `greenfield`, also capture the project idea, target user, success criteria, constraints, preferred stack if provided, and unknown decisions. If the user only gave a one-sentence idea, use `idea-refine` when needed to clarify user, success, and constraints before writing the executable spec.

For `brownfield`, use read-only discovery first. Prefer existing project facts over generic templates, reference existing documentation and configuration, and do not replace established conventions unless the user explicitly asks.

If a command is unknown, mark it as `Unknown` or `Not applicable` in `harness/tools/commands.md`; do not invent commands.

### 3. Bootstrap

Create or update these files from `assets/templates/`:

```text
AGENTS.md
harness/
├── specs/
├── context/
├── tools/
├── guardrails/
├── evals/
└── runs/
```

Use `scripts/init_harness.py` for deterministic scaffolding when creating the structure from scratch. Do not use `--force` for `brownfield` or `existing-harness` unless the user explicitly confirms overwriting harness files.

For `greenfield`, fill `harness/context/project-brief.md` and `harness/context/initialization-notes.md` from the user idea and discovered facts.

For `brownfield`, fill `harness/context/repo-map.md`, `architecture.md`, `coding-conventions.md`, `dependency-notes.md`, `tools/commands.md`, and `initialization-notes.md` from repository evidence.

For `existing-harness`, update only missing or clearly stale harness files. Preserve existing `AGENTS.md`, README, CI, tests, and code conventions unless the user confirms a rewrite.

### 4. Refine

For raw product ideas, vague project concepts, or early feature directions, use `idea-refine` before writing a spec. Save the one-page concept in the active run directory when the user confirms:

```text
harness/runs/YYYY-MM-DD-short-task-name/idea.md
```

The refined idea should define the problem statement, recommended direction, key assumptions, MVP scope, not-doing list, and open questions.

For `greenfield`, a one-sentence idea should normally produce both `idea.md` and an executable `spec.md`. Do not silently choose a technology stack; record missing stack decisions in the spec or make choosing the stack the first planned task.

### 5. Specify

For non-trivial tasks, use `spec-driven-development`. Save the resulting task contract in the active run directory:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

The spec must define objective, scope, non-goals, assumptions, acceptance criteria, verification, required evidence, context updates, and open questions. Do not use the spec step to generate the implementation plan.

### 6. Plan

After the spec is clear, use `task-planning`. Save the implementation plan in:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Tasks should be small, ordered by dependency, and include verification steps.

### 7. Execute

Implement against the active run only:

- Read `AGENTS.md`
- Read the active run's `idea.md` when present
- Read the active run's `spec.md` and `plan.md`
- Load only the needed files under `harness/context/`
- Check `harness/guardrails/` before edits
- Keep code changes scoped to the current spec

### 8. Verify

Run commands from `harness/tools/commands.md` and record results in `execution-log.md`.

### 9. Record

Each task run should use this structure:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── idea.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Use `idea.md` only when `idea-refine` was part of the run. Record changed files, commands run, verification results, unresolved risks, and whether each acceptance criterion passed.

### 10. Improve

After each run, review whether the harness itself needs improvement. Treat this as controlled maintenance of canonical harness files:

- Missing or stale context
- Unclear commands
- Weak guardrails
- Ambiguous evaluation criteria
- Repeated agent mistakes

For normal feature or bugfix runs, propose harness updates first and apply them only when the user approves or the project workflow explicitly allows harness maintenance. When the user asks to initialize, refine, or improve the harness, update the relevant harness files directly from evidence.

Update harness files, not unrelated application code, during this improvement phase. Keep changes small and traceable to the latest run, repository facts, or user-confirmed decisions.

## Related Skills

Read `references/related-skills.md` when deciding how this skill composes with existing skills. In short:

- Use bundled `idea-refine` for the Idea layer when a request is still exploratory.
- Use bundled `spec-driven-development` for the Spec layer.
- Use bundled `task-planning` for the Plan and Tasks layer.

## Boundaries

- Do not install this skill globally unless the user asks.
- Do not create a large agent platform before the project-level harness loop works.
- Do not invent commands that were not found or confirmed.
- Ask before adding dependencies, changing schemas, altering CI, or deleting tests.
- Never remove failing tests just to pass verification.

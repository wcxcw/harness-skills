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
- Confirm product shape before implementation: target audience, core workflow, information architecture, content/data sources, update model, and MVP quality bar must be explicit for product or content-driven projects.
- Confirm blocking decisions before implementation: technology stack, runtime, data model, core architecture, external services, deployment target, and major UX/platform choices must be confirmed or explicitly deferred as non-coding decision tasks.
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

For `greenfield`, also capture the project idea, target user, success criteria, constraints, product shape, preferred stack if provided, core implementation direction, and unknown decisions. If the user only gave a one-sentence idea, use `idea-refine` to clarify target audience, content/data scope, core user experience, success criteria, constraints, technology stack, and core approach before writing the executable spec.

For content-driven products such as news, directories, dashboards, or curated feeds, clarify content categories, source strategy, update cadence, ranking/filtering, page structure, and MVP quality bar before implementation. Do not turn a broad content product idea into a generic demo without confirming what the user wants the experience to be.

For `brownfield`, use read-only discovery first. Prefer existing project facts over generic templates, reference existing documentation and configuration, and do not replace established conventions unless the user explicitly asks.

If a command is unknown, mark it as `Unknown` or `Not applicable` in `harness/tools/commands.md`; do not invent commands.

### 3. Bootstrap

Create or update the minimal harness from `assets/templates/`:

```text
AGENTS.md
harness/
├── context/
│   ├── project-brief.md
│   └── initialization-notes.md
├── tools/
│   └── commands.md
├── feedback/
│   └── verification.md
├── guardrails/
│   └── boundaries.md
├── evals/
│   └── task-scorecard.md
└── runs/
```

Use `scripts/init_harness.py` for deterministic scaffolding when creating the structure from scratch:

- `--profile core` (default): minimal harness for new projects and general use.
- `--profile brownfield`: core plus repository context files for existing codebases.
- `--profile full`: every bundled template; use only when the user wants the expanded harness.

Do not use `--force` for `brownfield` or `existing-harness` unless the user explicitly confirms overwriting harness files.

For `greenfield`, fill `harness/context/project-brief.md` and `harness/context/initialization-notes.md` from the user idea and discovered facts.

For `brownfield`, use `--profile brownfield` when project context files are useful, then fill `harness/context/repo-map.md`, `architecture.md`, `coding-conventions.md`, `dependency-notes.md`, `tools/commands.md`, and `initialization-notes.md` from repository evidence.

For `existing-harness`, update only missing or clearly stale harness files. Preserve existing `AGENTS.md`, README, CI, tests, and code conventions unless the user confirms a rewrite.

Create optional files only when they remove real ambiguity or support a project need. Do not expand the harness just because templates exist.

### 4. Refine

For raw product ideas, vague project concepts, or early feature directions, use `idea-refine` before writing a spec. Save the one-page concept in the active run directory when the user confirms:

```text
harness/runs/YYYY-MM-DD-short-task-name/idea.md
```

The refined idea should define the problem statement, recommended direction, key assumptions, MVP scope, not-doing list, and open questions.

For `greenfield`, a one-sentence idea should normally produce both `idea.md` and an executable `spec.md`. Do not silently choose product shape, content scope, information architecture, technology stack, or core implementation approach. If product, technology, or architecture decisions are missing, ask the user before planning implementation, or make choosing them the first non-coding task.

### 5. Specify

For non-trivial tasks, use `spec-driven-development`. Save the resulting task contract in the active run directory:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

The spec must define objective, scope, non-goals, assumptions, acceptance criteria, verification, required evidence, context updates, and open questions. Do not use the spec step to generate the implementation plan.

Before moving to planning, block on unresolved decisions that would materially affect implementation:

- Target audience, primary use case, and success criteria
- Content/data scope, sources, update model, and editorial or quality bar
- Core user experience, information architecture, navigation, and key pages/views
- Technology stack, framework, runtime, or package manager
- Data storage, persistence model, or schema direction
- Authentication, authorization, permissions, or identity model
- External APIs, paid services, or infrastructure dependencies
- Deployment target, platform, or runtime environment
- Core UX flow or user-facing behavior

If the user does not want to decide yet, record the decision in `Open Questions` and make it the first task in `plan.md`. Do not write application code before that decision task is resolved.

### 6. Plan

After the spec is clear, use `task-planning`. Save the implementation plan in:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Tasks should be small, ordered by dependency, and include verification steps.

Do not proceed to execution if `spec.md` or `plan.md` contains unresolved blocking questions. Resolve them with the user or execute only the explicit non-coding decision task.

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

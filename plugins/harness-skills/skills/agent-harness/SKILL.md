---
name: agent-harness
description: Initialize and operate a project-level Agent Harness for software engineering work. Use when the user wants to create or update AGENTS.md, scaffold a minimal harness/ directory, define project context/tools/guardrails/gates, create run records, or combine bundled workflow skills into a repeatable Harness Engineering workflow.
---

# Agent Harness

## Overview

Use this skill to bootstrap and operate an Agent Harness: a controlled loop that tells agents what to do, what not to do, which context to load, which tools to use, how to record work, and how to evaluate completion.

This is an orchestration skill. Do not duplicate the full workflows of related skills. Use this skill to create the project harness and route work to the right supporting skill when needed.

## Operating Principles

- Clarify before coding: turn vague requests into explicit goals, constraints, and success criteria.
- Follow the user's language: if the user works in Chinese, generate harness files, run records, specs, plans, and explanations in Chinese unless the project already uses another language.
- Confirm product shape before implementation: target audience, core workflow, information architecture, content/data sources, update model, and MVP quality bar must be explicit for product or content-driven projects.
- Confirm blocking decisions before implementation: technology stack, runtime, data model, core architecture, external services, deployment target, and major UX/platform choices must be confirmed or explicitly deferred as non-coding decision tasks.
- Spec before implementation: non-trivial work needs a run-level spec before code changes.
- Plan into small verifiable tasks: each task should have scope, likely files, dependencies, and verification.
- Skip run creation for explicit, low-risk micro changes when no active run exists; make the edit, run the smallest relevant check, and summarize the result instead.
- Gate continuation locally: pass project-local gates before implementation and completion, using the smallest safe tier (`xs`, `standard`, or `full`).
- Keep run boundaries tied to user objectives: follow-up corrections, test fixes, verification additions, and small adjustments for the same objective stay in the active run.
- Evidence before completion: do not claim completion without commands, checks, or a documented reason verification was skipped.
- Keep scope small: prefer the simplest change that satisfies the spec; avoid unrelated refactors or speculative abstractions.
- Improve the harness from evidence: repeated failures, missing commands, stale context, or weak guardrails should feed back into canonical harness files.
- Treat canonical harness files as repository-owned collaboration assets. Personal notes and local run records must not replace the shared harness.

## Workflow

### 0. Decide Whether A Run Is Needed

Create a run only when the work needs a controlled record. A change is a
no-run micro change only when all of these are true:

- The user request is explicit and specific.
- The edit is local to one surface or one nearby file area.
- It does not change behavior, business logic, state flow, APIs, data shape,
  permissions, routing, validation, persistence, CI, dependencies, or schema.
- It does not require a product, design-direction, technical, architecture, or
  verification-strategy decision.
- It can be verified with a small targeted check.
- It can be reverted locally without broader impact.

For micro changes, make the edit directly, run the smallest relevant check, and
summarize the result in the response. If an active run already exists and the
micro change belongs to that objective, append the evidence to the active run.

Examples that may be no-run micro changes:

- Fix a typo or one sentence of copy.
- Change a named selector's font size from `18px` to `16px`.
- Adjust one button's spacing token or one color token.

Examples that are not micro changes:

- "Improve the homepage visuals."
- "Adjust the typography hierarchy."
- A change that spans multiple pages, alters interaction behavior, or needs a
  design decision.

Use `xs`, `standard`, or `full` when the task needs an audit trail, touches
project behavior, spans multiple concerns, requires a decision, or the user
explicitly asks to run it through the harness.

### 1. Choose Initialization Mode

Choose one mode before scaffolding or updating harness files:

- `greenfield`: Use when the project is empty, has no source or manifest files, or the user describes a new project from a short idea.
- `brownfield`: Use when the project already has source code, manifests, tests, CI, README, or other implementation history.
- `existing-harness`: Use when `AGENTS.md` or `harness/` already exists.

For `existing-harness`, preserve existing harness content by default. Add missing files, refresh stale placeholders, and propose larger rewrites only when the user asks.

### 2. Choose Output Language

Choose the harness language before writing files:

- Use the user's main language for generated harness content.
- If the user prompt is Chinese, use Chinese for `AGENTS.md`, `harness/context/*`, run records, `workflow.md`, `design.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, and `evaluation.md`.
- Keep code identifiers, commands, file paths, package names, framework names, and API names in their original language.
- For `brownfield`, prefer the existing project documentation language when it is consistent. If the user language and project language differ, use the user language for new run records and keep references to existing files unchanged.
- When scaffolding Chinese files with the script, pass `--language zh-CN`. Use `--language en` only when the project or user clearly prefers English.

### 3. Guided Initialization Gate

Use guided initialization before implementation when the project has only a short idea, the product shape is unclear, or blocking decisions are missing.

Use `brainstorming` for the actual clarifying questions and `design.md` output. Do not duplicate that workflow in this skill.

Do not write application code after asking the `brainstorming` questions. Wait for the user's answers, then update `project-brief.md`, create or update `workflow.md` and `design.md`, and proceed to spec only when the blocking decisions are answered or explicitly deferred as a non-coding decision task.

For content-driven products such as news, directories, dashboards, or curated feeds, this gate is required unless the user already provided content categories, source strategy, update cadence, ranking/filtering, page structure, and MVP quality bar.

### 4. Discover

Inspect the target project before writing harness files:

- Source layout and app type
- Package manager and runtime
- Build, test, lint, dev, and verification commands
- Existing documentation, CI, tests, and conventions

For `greenfield`, also capture the project idea, target user, success criteria, constraints, product shape, preferred stack if provided, core implementation direction, and unknown decisions. If the user only gave a one-sentence idea, use `brainstorming` to clarify target audience, content/data scope, core user experience, success criteria, constraints, technology stack, and core approach before writing the executable spec.

For content-driven products such as news, directories, dashboards, or curated feeds, clarify content categories, source strategy, update cadence, ranking/filtering, page structure, and MVP quality bar before implementation. Do not turn a broad content product idea into a generic demo without confirming what the user wants the experience to be.

For `brownfield`, use read-only discovery first. Prefer existing project facts over generic templates, reference existing documentation and configuration, and do not replace established conventions unless the user explicitly asks.

If a command is unknown, mark it as `Unknown` or `Not applicable` in `harness/tools/commands.md`; do not invent commands.

### 5. Bootstrap

Create or update the minimal harness from `assets/templates/`:

```text
AGENTS.md
harness/
├── context/
│   └── project-brief.md
├── controls/
│   └── gates.md
├── tools/
│   └── commands.md
├── guardrails/
│   └── boundaries.md
├── scripts/
│   └── check_run.py
└── runs/
```

Use `scripts/init_harness.py` for deterministic scaffolding when creating the structure from scratch:

- `--profile core` (default): the only supported scaffold profile. It creates the minimal harness, local gates, and run checker.
- `--language zh-CN`: Chinese harness templates.
- `--language en`: English harness templates.
- `--language auto` (default): follows process locale; prefer explicit `zh-CN` when the user prompt is Chinese.

Do not use `--force` for existing projects unless the user explicitly confirms overwriting harness files.

For `greenfield`, fill `harness/context/project-brief.md` from the user idea and discovered facts.

For `brownfield`, scaffold the same minimal core first. Add extra context files later only when repository evidence shows they remove real ambiguity.

For `existing-harness`, update only missing or clearly stale harness files. Preserve existing `AGENTS.md`, README, CI, tests, and code conventions unless the user confirms a rewrite.

Do not expand the harness just because templates exist.

Workflow skills may guide how the agent works, but local gates, commands, guardrails, and verification evidence remain authoritative.

### 6. Collaboration and Version Control

Use this ownership model for team projects:

- Commit canonical harness files to the repository: `AGENTS.md`, `harness/context/`, `harness/controls/`, `harness/tools/`, `harness/guardrails/`, and `harness/scripts/`.
- Treat `harness/runs/` as task-owned records. Commit run directories only when they are useful for review, audit, onboarding, future context, architecture decisions, or complex bug investigations.
- Do not maintain separate personal copies of the canonical harness as the source of truth. Personal notes may exist locally, but shared agent behavior should come from the repository harness.
- During normal feature or bugfix runs, write harness improvement proposals in the active run's `evaluation.md` instead of directly editing canonical harness files.
- Modify canonical harness files only in an explicit harness maintenance task, or when the user asks for harness initialization/improvement, or when the change is a factual correction from repository evidence.
- For multi-person repositories, recommend review protection or CODEOWNERS for `AGENTS.md` and canonical `harness/` directories.

If the project wants to keep most run records out of version control, recommend ignoring `harness/runs/*` while preserving `harness/runs/.gitkeep`, then force-add selected run directories when they matter.

### 7. Refine

For raw product ideas, vague project concepts, or early feature directions, use `brainstorming` before writing a spec. Save the one-page design in the active run directory when the user confirms:

```text
harness/runs/YYYY-MM-DD-short-task-name/design.md
```

The refined design should define the problem statement, recommended direction, key assumptions, MVP scope, not-doing list, and open questions.

For `greenfield`, a one-sentence idea should normally produce `workflow.md`, `design.md`, and an executable `spec.md`. Do not silently choose product shape, content scope, information architecture, technology stack, or core implementation approach. If product, technology, or architecture decisions are missing, ask the user before planning implementation, or make choosing them the first non-coding task.

### 8. Specify

For non-trivial tasks, use `writing-specs`. Save the resulting task contract in the active run directory:

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

### 9. Plan

After the spec is clear, use `writing-plans`. Save the implementation plan in:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Tasks should be small, ordered by dependency, and include verification steps.

Do not proceed to execution if `spec.md` or `plan.md` contains unresolved blocking questions. Resolve them with the user or execute only the explicit non-coding decision task.

### 10. Execute

Implement against the active run only:

- Read `AGENTS.md`
- Read the active run's `workflow.md` and `design.md` when present
- Read the active run's `spec.md` and `plan.md`
- Load only the needed files under `harness/context/`
- Check `harness/controls/gates.md`
- Check `harness/guardrails/` before edits
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier <xs|standard|full>` when an active run exists and the checker is available
- Keep code changes scoped to the current spec
- For user-requested corrections to the same objective, update the active run's `plan.md`, `execution-log.md`, or `evaluation.md` instead of creating a new run
- For direct micro changes with no active run, skip run artifacts and rely on the smallest relevant verification plus the final response summary

### 11. Verify

Run commands from `harness/tools/commands.md` and record results in `execution-log.md`.

Before claiming completion, run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier <xs|standard|full>` when an active run exists and the checker is available. If the checker cannot be run, record the reason in `execution-log.md`.

### 12. Record

When a run is warranted, use the smallest tier that safely controls the work.
Do not treat `xs` as mandatory for every tiny edit; no-run direct execution is
allowed for explicit, low-risk micro changes with no active run.
A run represents one user objective, not one agent attempt. Keep follow-up
corrections, test fixes, verification additions, and small adjustments in the
active run until the work is accepted or the run is closed. Create a new run
only when the objective changes, scope materially expands, or the user
explicitly starts a new task.

XS:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

Standard:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Full:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── workflow.md
├── design.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
└── evaluation.md
```

Use `design.md` for new feature or product direction work. Legacy runs may still contain `idea.md`. Record changed files, commands run, verification results, review findings, unresolved risks, and whether each acceptance criterion passed.

### 13. Improve

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

- Use bundled `brainstorming` for the Intake layer when a request is still exploratory.
- Use bundled `writing-specs` for the Spec layer.
- Use bundled `writing-plans` for the Plan layer.
- Use bundled execution, review, verification, and finishing workflows to close the run.

## Boundaries

- Do not install this skill globally unless the user asks.
- Do not create a large agent platform before the project-level harness loop works.
- Do not invent commands that were not found or confirmed.
- Ask before adding dependencies, changing schemas, altering CI, or deleting tests.
- Never remove failing tests just to pass verification.

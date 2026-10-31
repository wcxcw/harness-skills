---
name: agent-harness
description: Initialize and operate a project-level Agent Harness for software engineering work. Use when the user wants to create or update AGENTS.md, scaffold a minimal harness/ directory, define project context/tools/guardrails/gates, create run records, or combine bundled workflow skills into a repeatable Harness Engineering workflow.
---

# Agent Harness

## Overview

Use this skill to bootstrap and operate an Agent Harness: a controlled loop that tells agents what to do, what not to do, which context to load, which tools to use, how to record work, and how to evaluate completion.

This is an orchestration skill. Do not duplicate the full workflows of related skills. Use this skill to create the project harness and route work to the right supporting skill when needed.

## Operating Principles

- Align before creating a run: when the request is vague, the user may explicitly invoke `$grilling` to resolve decisions without files or implementation actions.
- Follow the user's language: if the user works in Chinese, generate harness files, run records, specs, plans, and explanations in Chinese unless the project already uses another language.
- Confirm product shape before implementation: target audience, core workflow, information architecture, content/data sources, update model, and MVP quality bar must be explicit for product or content-driven projects.
- Confirm blocking decisions before implementation: technology stack, runtime, data model, core architecture, external services, deployment target, and major UX/platform choices must be confirmed or explicitly deferred as non-coding decision tasks.
- Spec before implementation: non-trivial work needs a run-level spec before code changes.
- Plan into small verifiable tasks: each task should have scope, likely files, dependencies, and verification.
- Skip run creation for explicit, low-risk micro changes when no active run exists; make the edit, run the smallest relevant check, and summarize the result instead.
- Gate continuation locally: pass project-local gates before implementation and completion, using the smallest safe tier (`xs`, `standard`, or `full`).
- Load context on demand: do not bulk-read `harness/context/*` or completed runs; use targeted search or section reads.
- Keep run boundaries tied to user objectives: use the same run for follow-up corrections, test fixes, verification additions, and small adjustments; explicitly resume it if it is closed and the follow-up needs a run.
- Track run lifecycle explicitly in `run-state.json`; never infer the active run from directory modification time or artifact presence.
- Code quality is a completion gate: application code changes must preserve maintainable structure, local conventions, error handling, logging/observability where relevant, and useful comments for non-obvious rules.
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
When no run is active, a qualifying micro change may be done directly even if a
related run is closed; a closed run alone does not make `xs` necessary.

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

When the objective or material decisions are unclear, do not create the run
yet. Ask the user to explicitly invoke `$grilling` or provide the missing
decisions directly. Revisit run selection after shared understanding is
confirmed.

### 1. Choose Initialization Mode

Choose one mode before scaffolding or updating harness files:

- `greenfield`: Use when the project is empty, has no source or manifest files, or the user describes a new project from a short idea.
- `brownfield`: Use when the project already has source code, manifests, tests, CI, README, or other implementation history.
- `existing-harness`: Use when discovery confirms an existing project Harness. An `AGENTS.md` or directory named `harness/` alone does not establish ownership or compatibility.

For `existing-harness`, preserve existing harness content by default. Add missing files, refresh stale placeholders, and propose larger rewrites only when the user asks. If `harness/` exists but its role is unclear, inspect it before scaffolding; do not write into or replace an unrelated directory. If it is intentionally the project Harness but automatic detection cannot identify it, use `--adopt-existing` only after confirming that purpose from project evidence or the user's request.

### 2. Choose Output Language

Choose the harness language before writing files:

- Use the user's main language for generated harness content.
- If the user prompt is Chinese, use Chinese for `AGENTS.md`, `harness/context/*`, run records, `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, and `evaluation.md`.
- Keep code identifiers, commands, file paths, package names, framework names, and API names in their original language.
- For `brownfield`, prefer the existing project documentation language when it is consistent. If the user language and project language differ, use the user language for new run records and keep references to existing files unchanged.
- When scaffolding Chinese files with the script, pass `--language zh-CN`. Use `--language en` only when the project or user clearly prefers English.

### 3. Pre-Run Alignment Gate

Use pre-run alignment when the project has only a short idea, the product shape is unclear, or blocking decisions are missing.

`grilling` is explicitly user-invoked. When alignment is missing, recommend `$grilling` and stop before creating a run, scaffolding files, or writing application code. The user may instead provide the missing decisions directly.

During grilling, inspect the repository for facts, ask one decision question at a time with a recommended answer, and take no implementation action. After the user explicitly confirms shared understanding, bootstrap the Harness when needed, create the run, and let `writing-specs` record the confirmed decisions directly in `spec.md`.

For content-driven products such as news, directories, dashboards, or curated feeds, this gate is required unless the user already provided content categories, source strategy, update cadence, ranking/filtering, page structure, and MVP quality bar.

### 4. Discover

Inspect the target project before writing harness files:

- Source layout and app type
- Package manager and runtime
- Build, test, lint, dev, and verification commands
- Existing documentation, CI, tests, and conventions

For `greenfield`, also capture the project idea, target user, success criteria, constraints, product shape, preferred stack if provided, core implementation direction, and unknown decisions. If the user only gave a one-sentence idea, recommend explicit `$grilling` before creating a run; after confirmation, write the executable spec from that shared understanding.

For content-driven products such as news, directories, dashboards, or curated feeds, clarify content categories, source strategy, update cadence, ranking/filtering, page structure, and MVP quality bar before implementation. Do not turn a broad content product idea into a generic demo without confirming what the user wants the experience to be.

For `brownfield`, use read-only discovery first. Prefer existing project facts over generic templates, reference existing documentation and configuration, and do not replace established conventions unless the user explicitly asks. Inspect only task-relevant manifests, lockfiles, README, CI, scripts and existing harness files; a monorepo may require different working directories and commands for each component.

When useful, run `python3 <agent-harness-skill-dir>/scripts/discover_project.py --project <project-root>` for a read-only JSON inventory of common manifests, package script names and CI files. Resolve the script relative to this SKILL.md. It does not execute commands, install dependencies, or verify safety; its bounded scan and exclusions can miss project files. Inspect the actual relevant files before deciding which commands to run, and report any discovery errors or coverage gaps that affect the task.

Record command purpose, exact working directory, source and side effects in `harness/tools/commands.md`. Distinguish `Discovered` (explicit in a repository file or provided by the user), `Inferred` (plausible but not confirmed), `Verified` (executed in a stated environment with result and date), `Failed`, `Unknown`, and `Not applicable` (evidence shows it is not relevant). A documented command is not automatically verified in the current environment. Preserve a project's existing status vocabulary, such as `Confirmed`, without treating it as fresh execution evidence.

Do not invent commands or run `Unknown` or `Inferred` commands. Verify relevant commands only when appropriate for the task and permissions, using the least disruptive useful check. First inspect command and script behavior and prerequisites; do not execute commands solely because they appear in a manifest. Installation, server startup, migrations, deployment, external calls or tests may mutate data, access a network or consume credentials. Respect the user's authorization, project rules and sandbox; record skipped checks and their reason. A failed or skipped attempt is not `Verified`.

For behavior changes choose actual feedback where available: relevant tests and build checks, browser interaction and console errors for UI, API responses and errors for services, or output and exit codes for CLI tasks. Prefer existing project tools; do not require installing a new stack merely to complete initialization. Record command, working directory, date, exit status, and environment/limitations, without secrets.

For existing harnesses, keep context loading selective. Read the concise
`project-brief.md`, `gates.md`, `commands.md`, and `boundaries.md` first, then
read only the active run and context files required by the task. Do not load all
`harness/context/*` or all completed run records during routine work.

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
- `--update-checker`: refresh only `harness/scripts/check_run.py` in an existing Harness after gate-schema updates; all other project files are preserved.
- `--adopt-existing`: explicitly use an inspected nonempty `harness/` directory that the scaffold cannot identify; it does not overwrite files by itself.

Do not use `--force` for existing projects unless the user explicitly confirms overwriting harness files.

For `greenfield`, fill `harness/context/project-brief.md` from the user idea and discovered facts.

For `brownfield`, scaffold the same minimal core first. Add extra context files later only when repository evidence shows they remove real ambiguity.

For `existing-harness`, update only missing or clearly stale harness files within the user's authorized task. Preserve existing `AGENTS.md`, README, CI, tests, and code conventions unless a rewrite is requested. `--update-checker` is an explicit replacement of the local checker; do not use it as a routine initialization step over a customized checker.

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

### 7. Start From Confirmed Alignment

For raw product ideas, vague project concepts, or early feature directions, complete explicit `$grilling` before creating a run. Grilling stays conversational and creates no Harness artifacts.

Once the user confirms shared understanding, create the selected run tier and record the problem, scope, decisions, acceptance criteria, and open questions in `spec.md` when required by the tier. A clear user request already establishes alignment for what it specifies; record its source rather than requesting duplicate confirmation. Ask only about unresolved decisions that materially block work.

After creating or explicitly resuming a run, bind it to the current session:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --tier <xs|standard|full> --set-phase active
```

This writes `run-state.json` with a hashed session identifier. If no run is
created or resumed, do not create state merely because another run is the most
recent directory on disk. When supported by the checker, first activation also
captures the Git HEAD baseline; retain it across phase changes and resumption so
quality checks can include commits made during the run. A pre-existing run that
has no baseline, a repository with no initial commit, or a non-Git project cannot
reconstruct prior committed changes reliably; record that coverage limitation.
For a follow-up to the same objective that needs a run, explicitly select and
resume its existing run even if it is closed. Do not infer the run from recency.
Before resuming, check its state; do not rebind a run active in another session.
The checker does not provide concurrent-session locking, so avoid simultaneous
edits to the same run.
Append the new work and evidence, preserve prior evaluation history, update the
current evaluation, and perform fresh checks and any applicable review before
closing it again. The original Git baseline is retained on resumption and may
include unrelated later commits; inspect the actual scope and document any
coverage limitation rather than treating old evidence as proof of new work.

### 8. Specify

For non-trivial tasks, use `writing-specs`. Save the resulting task contract in the active run directory:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

The spec must record the alignment source (including a clear original request when applicable), then define objective, scope, non-goals, assumptions, product and technical decisions, acceptance criteria, verification, required evidence, context updates, and open questions. Do not use the spec step to generate the implementation plan. XS runs do not require a spec or plan; use those artifacts only when the chosen tier or task needs them.

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

For tiers that require a spec and plan, after the spec is clear use `writing-plans`. Save the implementation plan in:

```text
harness/runs/YYYY-MM-DD-short-task-name/plan.md
```

Tasks should be small, ordered by dependency, and include verification steps.

Do not proceed to execution if `spec.md` or `plan.md` contains unresolved blocking questions. Resolve them with the user or execute only the explicit non-coding decision task.

### 10. Execute

Implement against the active run only:

- Read `AGENTS.md`
- Read the active run's `workflow.md`, `spec.md`, and `plan.md` when required by the tier or present and relevant; XS need not create them
- Load only the needed files under `harness/context/`; use targeted search or section reads for large context files
- Check `harness/controls/gates.md`
- Check `harness/guardrails/` before edits
- Run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier <xs|standard|full>` when an active run exists and the checker is available
- Keep code changes scoped to the current spec
- For user-requested corrections to the same objective that need a run, continue or explicitly resume the existing run and update its relevant plan, execution log, and evaluation instead of creating a new run
- When resuming implementation after review or a failed gate, set the current run phase back to `active`
- For direct micro changes with no active run, skip run artifacts and rely on the smallest relevant verification plus the final response summary

### 11. Verify

Select relevant project commands from `harness/tools/commands.md`, verify their prerequisites and side effects, and record actual results in `execution-log.md`. Create an `evaluation.md` draft before invoking the completion gate; then finalize it with verification and risk evidence before the final gate and `verifying` transition.

Before claiming completion, run `python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier <xs|standard|full>` when an active run exists and the checker is available. If the checker cannot be run, record the reason in `execution-log.md`.

After `finishing-run` has finalized `evaluation.md` and the explicit completion
gate passes, mark the current session as ready for the Stop-hook safety check:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --tier <xs|standard|full> --set-phase verifying
```

Set `verifying` only immediately before the final completion response. The Stop
hook re-runs the completion and quality gates for that session and changes the
state to `closed` on success. Pure conversation, `active`, `reviewing`, closed,
legacy stateless, and other-session runs are not Stop-gated. On platforms
without the Harness Stop hook, set `closed` explicitly after the final gate:

```text
python3 harness/scripts/check_run.py harness/runs/<run> --tier <xs|standard|full> --set-phase closed
```

### 12. Record

When a run is warranted, use the smallest tier that safely controls the work.
Do not treat `xs` as mandatory for every tiny edit; no-run direct execution is
allowed for explicit, low-risk micro changes with no active run.
A run represents one user objective, not one agent attempt or response. For
follow-up corrections, test fixes, verification additions, and small adjustments
that need a run, continue or explicitly resume the same run even after closure.
Create a new run when the objective changes, scope materially expands, or the
user explicitly requests a separate task or record.

XS:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
├── run-state.json
└── evaluation.md
```

Standard:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
├── run-state.json
└── evaluation.md
```

Full:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
├── run-state.json
└── evaluation.md
```

Legacy runs may still contain `design.md` or `idea.md`; new runs record confirmed decisions directly in `spec.md`. Record changed files, commands run, verification results, review findings, unresolved risks, and whether each acceptance criterion passed.

### 13. Improve

After each run, review whether the harness itself needs improvement. In `evaluation.md`, record a concrete issue, its evidence, a proposed change, and status (`pending`, `applied`, or `not adopted`); record the verification result when applied. State `none` when no improvement is identified. Treat this as controlled maintenance of canonical harness files:

- Missing or stale context
- Unclear commands
- Weak guardrails
- Ambiguous evaluation criteria
- Repeated agent mistakes

For normal feature or bugfix runs, propose harness updates first and apply them when the user's instructions or the project workflow authorize harness maintenance. When the user asks to initialize, refine, or improve the harness, update the relevant harness files directly from evidence. Do not build a separate feedback tracker unless the project needs one.

Update harness files, not unrelated application code, during this improvement phase. Keep changes small and traceable to the latest run, repository facts, or user-confirmed decisions.

## Related Skills

Read `references/related-skills.md` when deciding how this skill composes with existing skills. In short:

- Use bundled `grilling` before creating a run, only when the user explicitly invokes it to resolve an exploratory request.
- Use bundled `writing-specs` for the Spec layer.
- Use bundled `writing-plans` for the Plan layer.
- Use bundled `context-budget` when project context or run history could become large.
- Use bundled execution, code quality review, receiving-review, verification, and finishing workflows to close the run.

## Boundaries

- Do not install this skill globally unless the user asks.
- Do not create a large agent platform before the project-level harness loop works.
- Do not invent commands that were not found or confirmed.
- Ask before adding dependencies, changing schemas, altering CI, or deleting tests.
- Never remove failing tests just to pass verification.

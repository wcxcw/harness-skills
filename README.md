# Harness Skills

[中文](README.zh-CN.md)

A Codex skill pack for creating and operating a project-level Agent Harness.

Harness Engineering gives agents a controlled workspace: specs, curated context, approved commands, guardrails, run records, and evaluation loops. This pack turns that structure into reusable Codex skills and templates.

## What It Does

- Creates a project-level `AGENTS.md` and `harness/` workspace
- Supports new projects, existing codebases, and existing harnesses
- Keeps idea refinement, specs, plans, execution logs, verification, and evaluation in one workflow
- Lets agents propose or apply targeted harness updates after each run, based on run evidence and user-confirmed decisions

## Core Principles

- Clarify before coding
- Spec before implementation
- Plan into small, verifiable tasks
- Require evidence before completion
- Feed run results back into the harness

## Included Skills

| Skill | Purpose |
| --- | --- |
| `agent-harness` | Main orchestration skill for initializing, running, and maintaining the harness. |
| `idea-refine` | Converts raw ideas into a compact `idea.md` brief. |
| `spec-driven-development` | Converts unclear work into a run-level `spec.md`. |
| `task-planning` | Converts an accepted spec into scoped, ordered tasks in `plan.md`. |

## Usage

Use one of these prompts. `agent-harness` chooses `greenfield`, `brownfield`, or `existing-harness` mode from the project state.

### New Project

```text
Use agent-harness to start a new project from this idea: a lightweight habit tracker for remote teams.
```

### Existing Project

```text
Use agent-harness to initialize an Agent Harness for this existing codebase.
```

### Run a Task

```text
Use agent-harness to run this task through the harness: add tag filtering to the issue list.
```

## Repository Layout

```text
harness-skills/
├── README.md
├── README.zh-CN.md
├── docs/
└── skills/
    ├── agent-harness/
    ├── idea-refine/
    ├── spec-driven-development/
    └── task-planning/
```

Main entry point:

```text
skills/agent-harness/SKILL.md
```

Templates used by the main skill:

```text
skills/agent-harness/assets/templates/
```

## Initialization Modes

| Mode | Use When | Default Behavior |
| --- | --- | --- |
| `greenfield` | Empty project or one-sentence project idea | Refine the idea when needed, create a project brief, then produce an executable spec and plan. |
| `brownfield` | Existing source code, manifests, tests, CI, or README | Run read-only discovery, document facts, and add harness files conservatively. |
| `existing-harness` | `AGENTS.md` or `harness/` already exists | Preserve existing harness content, fill gaps, and avoid overwriting conventions. |

## Generated Harness

```text
AGENTS.md
harness/
├── specs/
│   ├── feature-template.md
│   └── bugfix-template.md
├── context/
│   ├── project-brief.md
│   ├── initialization-notes.md
│   ├── repo-map.md
│   ├── architecture.md
│   ├── coding-conventions.md
│   └── dependency-notes.md
├── tools/
│   ├── commands.md
│   └── verification.md
├── guardrails/
│   ├── permissions.md
│   ├── boundaries.md
│   └── rollback.md
├── evals/
│   ├── acceptance-checklist.md
│   ├── regression-checklist.md
│   └── task-scorecard.md
└── runs/
```

## Run Records

Each agent task should use a run directory:

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── idea.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

Use `idea.md` only when the run included idea refinement.

| File | Purpose |
| --- | --- |
| `input.md` | Original user request. |
| `idea.md` | Refined problem, direction, assumptions, MVP scope, and non-goals. |
| `spec.md` | Objective, scope, assumptions, acceptance criteria, verification, and required evidence. |
| `plan.md` | Ordered tasks, dependencies, likely files, verification, and required evidence. |
| `execution-log.md` | Files changed, commands run, test results, failures, and skipped checks. |
| `evaluation.md` | Spec compliance, regression risk, residual risks, and harness feedback. |

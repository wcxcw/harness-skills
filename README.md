# Harness Skills

A Codex skill pack for applying Harness Engineering to real software projects.

Harness Engineering gives agents a controlled project workspace: clear specs, curated context, approved tools, feedback loops, guardrails, evaluations, and persistent run records. This pack bundles the skills needed to initialize and operate that workflow.

## What This Pack Does

Use this pack when you want Codex to:

- Create or update a project-level `AGENTS.md`
- Scaffold a `harness/` directory
- Initialize either a new project, an existing codebase, or an existing harness
- Refine raw ideas into focused one-page concepts
- Turn requests into specs before coding
- Break specs into small, verifiable tasks
- Run implementation work through explicit guardrails
- Record each agent run for review and iteration

The intended flow is:

```text
User request
-> Idea refinement, when needed
-> Spec
-> Plan
-> Task execution
-> Verification
-> Run record
-> Evaluation
-> Harness improvement
```

## Included Skills

| Skill | Purpose |
| --- | --- |
| `agent-harness-bootstrap` | Main orchestration skill. Initializes and operates the Harness Engineering workflow. |
| `idea-refine` | Turns raw ideas into focused one-page concepts before specification. |
| `spec-driven-development` | Turns ambiguous or multi-file work into a reviewed specification. |
| `planning-and-task-breakdown` | Breaks a validated spec into ordered, verifiable implementation tasks. |

## Repository Layout

```text
harness-skills/
├── README.md
└── skills/
    ├── agent-harness-bootstrap/
    ├── idea-refine/
    ├── spec-driven-development/
    └── planning-and-task-breakdown/
```

The main entry point is:

```text
skills/agent-harness-bootstrap/SKILL.md
```

The Harness templates used by that skill live under:

```text
skills/agent-harness-bootstrap/assets/templates/
```

## Usage

Use one of these three entry prompts. The skill chooses `greenfield`, `brownfield`, or `existing-harness` mode from the project state.

### New Project

Start from a short idea:

```text
Use agent-harness-bootstrap to start a new project from this idea: a lightweight habit tracker for remote teams.
```

### Existing Project

Initialize or refresh the harness for an existing codebase:

```text
Use agent-harness-bootstrap to initialize an Agent Harness for this existing codebase.
```

### Run a Task

Run a feature, bugfix, implementation step, or harness improvement through the harness:

```text
Use agent-harness-bootstrap to run this task through the harness: add tag filtering to the issue list.
```

## Generated Harness Structure

The bootstrap workflow supports three initialization modes:

| Mode | Use When | Default Behavior |
| --- | --- | --- |
| `greenfield` | Empty project or one-sentence project idea | Refine the idea when needed, create a project brief, then produce an executable spec and plan. |
| `brownfield` | Existing source code, manifests, tests, CI, or README | Run read-only discovery, document facts, and add harness files conservatively. |
| `existing-harness` | `AGENTS.md` or `harness/` already exists | Preserve existing harness content, fill gaps, and avoid overwriting conventions. |

The bootstrap workflow creates a project-level structure like this:

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

Each agent task should create a run directory:

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

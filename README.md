# Harness Skills

A Codex skill pack for applying Harness Engineering to real software projects.

Harness Engineering gives agents a controlled project workspace: clear specs, curated context, approved tools, feedback loops, guardrails, evaluations, and persistent run records. This pack bundles the skills needed to initialize and operate that workflow.

## What This Pack Does

Use this pack when you want Codex to:

- Create or update a project-level `Agents.md`
- Scaffold a `harness/` directory
- Turn requests into specs before coding
- Break specs into small, verifiable tasks
- Run implementation work through explicit guardrails
- Record each agent run for review and iteration
- Verify browser-facing behavior when the runtime supports it

The intended flow is:

```text
User request
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
| `spec-driven-development` | Turns ambiguous or multi-file work into a reviewed specification. |
| `planning-and-task-breakdown` | Breaks a validated spec into ordered, verifiable implementation tasks. |
| `browser-testing-with-devtools` | Guides real browser verification for web projects. |

## Repository Layout

```text
harness-skills/
├── README.md
└── skills/
    ├── agent-harness-bootstrap/
    ├── spec-driven-development/
    ├── planning-and-task-breakdown/
    └── browser-testing-with-devtools/
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

Initialize Harness Engineering in a project:

```text
Use agent-harness-bootstrap to initialize an Agent Harness for this project.
```

Create a run for a concrete task:

```text
Use agent-harness-bootstrap to create a harness run for this task: add tag filtering to the issue list.
```

Execute from an existing run:

```text
Use agent-harness-bootstrap to implement the current harness run and record execution-log.md and evaluation.md.
```

Improve the harness after a failed or noisy run:

```text
Use agent-harness-bootstrap to review the latest run and update the harness guardrails, commands, or context.
```

## Generated Harness Structure

The bootstrap workflow creates a project-level structure like this:

```text
Agents.md
harness/
├── specs/
│   ├── feature-template.md
│   └── bugfix-template.md
├── context/
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
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

## Runtime Notes

All listed skill directories are bundled in this repository, but some skills still need compatible tools in the user's Codex environment:

- `browser-testing-with-devtools` needs browser and DevTools access.

Bundling the skill files makes them distributable together. It does not guarantee every external runtime, MCP server, browser integration, or DevTools dependency exists on every machine.

## Publishing Notes

This pack vendors skills from the local environment. Before public release, review licensing and redistribution terms for bundled skills and assets, especially:

- `browser-testing-with-devtools`

If redistribution is not allowed or unclear, publish only `agent-harness-bootstrap` and document the others as prerequisites.

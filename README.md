# Harness Skills

[中文](README.zh-CN.md)

Harness Skills is a Codex plugin for bootstrapping and operating a project-level Agent Harness.

It does not replace an application project and it is not just a workflow skill collection. It initializes a controlled workspace that agents can use consistently: project context, specs, plans, approved commands, guardrails, run records, local gates, and evaluation feedback.

## Positioning

```text
harness-skills
= Codex plugin
= Agent Harness bootstrap scaffold
= project-level control system templates
= workflow skills + local gates + run artifacts
```

## When To Use

- A new project starts from a one-sentence idea and needs clarification before implementation.
- An existing codebase needs an agent-readable `AGENTS.md` and `harness/` workspace.
- Agent tasks should produce specs, plans, execution evidence, and evaluation records.
- Completion should be checked by local gates instead of a verbal "done".
- Small tasks should stay light while complex work can use a full closed loop.

## Install

Install through a Git marketplace:

```text
codex plugin marketplace add wcxcw/harness-skills --ref main
codex plugin add harness-skills@harness-skills
```

## Main Skills

| Skill | Purpose |
| --- | --- |
| [`agent-harness`](plugins/harness-skills/skills/agent-harness/SKILL.md) | Main entry point for initializing, running, and maintaining a project harness. |
| [`workflows`](plugins/harness-skills/skills/workflows/SKILL.md) | Closed-loop workflows for brainstorming, specs, plans, execution, debugging, review, verification, and finishing. |
| [`meta`](plugins/harness-skills/skills/meta/SKILL.md) | Skills for maintaining and improving Harness skills themselves. |

## Generated Harness

The default `core` scaffold creates:

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

You can also run the scaffold script directly:

```text
python3 plugins/harness-skills/skills/agent-harness/scripts/init_harness.py --project /path/to/project --language en
```

## Closed Loop

A full run follows:

```text
intake/design
  -> spec
  -> plan
  -> before-implementation gate
  -> execute
  -> review
  -> verification
  -> evaluation
  -> harness feedback
```

Run artifacts:

| File | Purpose |
| --- | --- |
| `workflow.md` | Skills used, lifecycle decisions, and gate status. |
| `design.md` | Refined problem, target user, recommended direction, MVP, non-goals, and open questions. |
| `spec.md` | Objective, scope, assumptions, acceptance criteria, verification, and required evidence. |
| `plan.md` | Ordered tasks, dependencies, likely files, verification, and evidence requirements. |
| `execution-log.md` | Files changed, commands run, test results, failures, and skipped checks. |
| `review.md` | Review scope, findings, resolution, and remaining risk. |
| `evaluation.md` | Acceptance, verification, review status, residual risk, and harness feedback. |

## Run Tiers

Use the smallest tier that safely controls the work when a run is warranted.

No-run direct changes are allowed only when all micro-change criteria are met:
the request is explicit, local, behavior-preserving, decision-free, easy to
verify with one targeted check, and locally reversible. Examples: typo fixes,
one sentence of copy, one named selector font-size change, or one spacing/color
token. Broad visual improvements, typography hierarchy changes, cross-page
changes, behavior changes, or work requiring a design/product/technical
decision should use the smallest run tier instead.

A run tracks one user objective, not each agent attempt. Follow-up corrections,
test fixes, verification additions, and small adjustments for the same objective
should append to the active run until the user accepts the work or the run is
closed. Create a new run only when the objective changes, the scope materially
expands, or the user explicitly starts a new task.

### XS

For small changes that still need a run record, such as low-risk
documentation/config/code edits with verification evidence.

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

### Standard

For most features, bugfixes, and structured changes.

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

### Full

For greenfield work, new product direction, complex bugs, or higher-risk changes.

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

## Local Gates

Generated projects include `harness/scripts/check_run.py` to check whether the active run satisfies the selected tier before implementation and completion.

Workflow skills help the agent work, but they do not bypass project-local gates.

## Initialization Modes

| Mode | Use when | Default behavior |
| --- | --- | --- |
| `greenfield` | Empty project or one-sentence idea | Clarify direction, then create project brief, spec, and plan. |
| `brownfield` | Existing source, README, tests, CI, or dependency manifests | Run read-only discovery, then add harness files conservatively. |
| `existing-harness` | `AGENTS.md` or `harness/` already exists | Preserve existing conventions, fill gaps, and avoid overwrites. |

## Language

- Chinese user prompts should generate Chinese `AGENTS.md`, `harness/context/*`, `workflow.md`, `design.md`, `spec.md`, `plan.md`, and run records by default.
- Commands, paths, package names, framework names, and API names stay in their original language.
- Existing projects should respect the established documentation language when it is consistent.

Use Chinese templates explicitly:

```text
python3 plugins/harness-skills/skills/agent-harness/scripts/init_harness.py --project /path/to/project --language zh-CN
```

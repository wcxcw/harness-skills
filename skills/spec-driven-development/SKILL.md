---
name: spec-driven-development
description: Create a run-level executable spec before implementation. Use for new projects, features, bugfixes, or significant changes when requirements, scope, acceptance criteria, or verification are not yet explicit.
---

# Spec-Driven Development

Create the task contract before implementation. The spec defines what will change, what will not change, how success will be judged, and what evidence is required before completion.

This skill only owns `spec.md`. Planning belongs to `task-planning`; execution belongs to the active harness run.

## Harness Output

Save the final spec to the active harness run:

```text
harness/runs/YYYY-MM-DD-short-task-name/spec.md
```

If no active run exists, create or ask for the intended run directory under `harness/runs/`. Do not create a separate documentation directory.

## Scope Boundary

This skill creates a run-level executable spec. It may reference project-level rules, but it does not own canonical harness files.

- Read canonical commands from `harness/tools/commands.md` when available.
- Read canonical coding conventions from `harness/context/coding-conventions.md` when available.
- Read canonical boundaries from `harness/guardrails/` when available.
- Record missing or stale project-level rules in `Context Updates` or `Open Questions`.
- Do not edit canonical harness files during spec writing unless the user asked for harness maintenance or the active workflow explicitly allows it.

## Spec Principles

- Clarify before coding.
- Confirm material assumptions before locking scope.
- Block implementation when product shape, content/data scope, or core user experience is unconfirmed.
- Block implementation when technology stack or core approach is unconfirmed.
- Define success in testable terms.
- Define required evidence before implementation.
- Keep scope small and name non-goals.
- Prefer project evidence over generic defaults.

## Default Flow

1. Read `idea.md` when present, then relevant harness context and project facts.
2. Restate the request as objective, scope, and non-goals.
3. List material assumptions. Ask the user when an assumption changes product behavior, content/data scope, information architecture, core UX, technology stack, architecture, data, security, cost, deployment, or timeline.
4. Convert vague requirements into success criteria and acceptance criteria.
5. Mark blocking decisions as confirmed, inferred from repository evidence, or `Needs decision`.
6. Define verification and evidence required before completion.
7. Record context or harness gaps in `Context Updates`.
8. Ask the user to confirm the spec before planning or implementation.

Do not generate an implementation plan in this skill. If the spec is accepted, use `task-planning` next.

## Spec Template

```markdown
# Spec: [Project/Feature/Fix Name]

## Context Source
- Source: [user input | idea.md | brownfield audit | bug report | existing spec]
- Initialization mode: [greenfield | brownfield | existing-harness]

## Objective
[What should be true when this is complete, and why it matters.]

## Target User
[Specific user, operator, system, or stakeholder affected by the change.]

## In Scope
- [Behavior, capability, or fix included.]
- [Behavior, capability, or fix included.]

## Out of Scope
- [Explicit non-goal.]
- [Explicit non-goal.]

## Assumptions
- [Assumption and whether it is confirmed, inferred, or needs confirmation.]

## Product Decisions
- Target audience: [Confirmed value, inferred from user input, or "Needs decision"]
- Core use case: [Confirmed value or "Needs decision"]
- Information architecture: [Key pages/views/navigation or "Needs decision"]
- Content/data scope: [Categories, sources, update model, or "Needs decision"]
- Quality bar: [MVP quality expectations, editorial rules, freshness, performance, or "Needs decision"]

## Technical Decisions
- Stack/runtime: [Confirmed value, inferred project default, or "Needs decision"]
- Core approach: [Confirmed approach, inferred project pattern, or "Needs decision"]
- Data/storage: [Confirmed value, inferred project default, "Not applicable", or "Needs decision"]
- External services: [Confirmed value, "None", or "Needs decision"]
- Deployment/runtime target: [Confirmed value, inferred project default, or "Needs decision"]

## Acceptance Criteria
- [ ] [Specific, observable condition.]
- [ ] [Specific, observable condition.]
- [ ] Existing relevant behavior does not regress.

## Verification
- [ ] [Command or manual check.]
- [ ] [Command or manual check.]

## Evidence Required
- [Command output, test result, manual check, or artifact needed before this can be called complete.]

## Constraints
- [Technical, product, data, security, timeline, or compatibility constraint.]

## Context Updates
- [Project-level commands, conventions, guardrails, or context that may need to be added or changed. Use "None" if not needed.]

## Open Questions
- [Question needing user input before planning or implementation. Use "None" if resolved.]
```

## Blocking Questions

Do not hand off to planning or implementation while a `Product Decisions` or `Technical Decisions` item is `Needs decision`, unless the next plan task is explicitly a non-coding decision task.

Blocking decisions include target audience, core use case, content/data scope, information architecture, core UX, quality bar, technology stack, runtime, framework, data model, authentication, external services, deployment target, and core user-facing behavior.

## Quality Bar

Before handing off to planning:

- [ ] Objective is clear.
- [ ] Scope and non-goals are explicit.
- [ ] Assumptions are visible.
- [ ] Product decisions are confirmed, inferred from user input or repository evidence, or explicitly deferred as a non-coding decision task.
- [ ] Technical decisions are confirmed, inferred from repository evidence, or explicitly deferred as a non-coding decision task.
- [ ] Acceptance criteria are testable.
- [ ] Verification and required evidence are defined.
- [ ] Open questions are resolved or explicitly carried forward.
- [ ] The spec is saved to the active `harness/runs/.../spec.md`.

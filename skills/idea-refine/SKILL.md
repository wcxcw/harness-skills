---
name: idea-refine
description: Refine raw project or feature ideas into a compact harness-ready brief. Use when the user starts from a vague idea, one-sentence project description, or early product direction before writing a spec.
---

# Idea Refine

Turn a raw idea into a concise `idea.md` that can feed `spec-driven-development`.

This skill is intentionally lightweight by default. Use the advanced references only when the user explicitly asks for broader ideation, alternatives, or stress-testing.

## Output Language

Use the user's main language for `idea.md`. If the user describes the idea in Chinese, write the brief and clarifying questions in Chinese. Keep code identifiers, product names, API names, file paths, and technology names in their original language.

## Harness Output

Save the final brief to the active harness run:

```text
harness/runs/YYYY-MM-DD-short-task-name/idea.md
```

If no active run exists, create or ask for the intended run directory under `harness/runs/`. Do not create a separate ideas directory.

## Default Flow

Use this path for harness initialization, greenfield projects, and short feature ideas.

1. Restate the idea as a clear problem statement.
2. Ask clarifying questions when product shape is unclear. For vague product ideas, ask at most 5 focused questions to identify target user, first-version shape, content/data scope, core user experience, success criteria, constraints, technology stack, and core approach.
3. Identify the target user, desired outcome, content/data sources, core workflow, constraints, preferred stack, core approach, and key assumptions.
4. Propose 1 recommended direction and, only if useful, 1-2 alternatives.
5. Define the smallest MVP that tests the core assumption.
6. Make the `Not Doing` list explicit.
7. Ask the user to confirm before saving `idea.md` or moving to spec.

Do not run a full brainstorming workshop by default. The goal is a buildable brief, not a large idea catalogue.

For one-sentence greenfield ideas, do not silently fill major product or technical choices. Ask first, or mark the item as `Needs decision` and keep implementation blocked until the decision is resolved.

## Guided Questions

Use these as the default question set for one-sentence greenfield ideas. Adapt wording to the user's language and project type.

1. Who is the target user, and what frequent problem should this solve?
2. What should the first version be: website, dashboard, tool, API, automation, backend service, or something else?
3. What content, data sources, inputs, outputs, or update cadence does the first version need?
4. What technology stack, runtime, deployment target, or "must not use" constraints should be respected?
5. What counts as success for the first version, and what is explicitly out of scope?

## Advanced Mode

Use advanced mode only when the user asks to ideate, compare directions, stress-test, or explore alternatives.

- Read `frameworks.md` when you need additional ideation lenses.
- Read `refinement-criteria.md` when you need a fuller evaluation rubric.
- Read `examples.md` only when you need output style examples.

Even in advanced mode, prefer 3-5 strong directions over many shallow ones.

## Brief Template

```markdown
# [Idea Name]

## Problem Statement
[One-sentence framing of the problem or opportunity.]

## Target User
[Specific user or buyer. Avoid "everyone".]

## Success Criteria
- [Specific outcome that would make this worth building.]
- [Specific outcome that would prove the MVP works.]

## Content or Data Scope
- [Content categories, data sources, update cadence, editorial rules, or "Needs decision".]

## Core User Experience
- [Primary pages, workflows, navigation model, and what makes the experience useful.]

## Recommended Direction
[The chosen direction and why. Keep this to 1-2 short paragraphs.]

## Constraints
- [Time, tech, budget, platform, compliance, or project constraints.]

## Preferred Stack
- [Confirmed stack, user preference, or "Needs decision".]

## Core Approach
[Core implementation direction or "Needs decision".]

## Key Assumptions to Validate
- [ ] [Assumption 1 and how to test it.]
- [ ] [Assumption 2 and how to test it.]
- [ ] [Assumption 3 and how to test it.]

## MVP Scope
[The smallest version that tests the core assumption.]

## Not Doing
- [Explicit non-goal and why.]
- [Explicit non-goal and why.]

## Open Questions
- [Question that needs answering before spec or implementation.]
```

## Guardrails

- Do not proceed without a target user and success criteria.
- Do not proceed with content-driven products until content scope, source strategy, update model, and core user experience are explicit or marked `Needs decision`.
- Do not silently choose a technology stack or core implementation approach; ask the user or record it as `Needs decision`.
- Do not turn the idea brief into an implementation plan. Planning belongs in `plan.md`.
- Do not over-expand a simple idea. Prefer the shortest useful path to a spec.
- If inside an existing codebase, ground assumptions in repository evidence when available.

## Verification

Before handing off to spec:

- [ ] Problem statement is clear.
- [ ] Target user is specific.
- [ ] Success criteria are testable.
- [ ] Product shape, content/data scope, and core user experience are clear or marked `Needs decision`.
- [ ] Preferred stack and core approach are confirmed or marked `Needs decision`.
- [ ] MVP scope is small enough to build first.
- [ ] Key assumptions and non-goals are explicit.
- [ ] User confirmed the direction or unresolved questions are recorded.

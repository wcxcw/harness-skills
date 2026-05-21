---
name: idea-refine
description: Refine raw project or feature ideas into a compact harness-ready brief. Use when the user starts from a vague idea, one-sentence project description, or early product direction before writing a spec.
---

# Idea Refine

Turn a raw idea into a concise `idea.md` that can feed `spec-driven-development`.

This skill is intentionally lightweight by default. Use the advanced references only when the user explicitly asks for broader ideation, alternatives, or stress-testing.

## Harness Output

Save the final brief to the active harness run:

```text
harness/runs/YYYY-MM-DD-short-task-name/idea.md
```

If no active run exists, create or ask for the intended run directory under `harness/runs/`. Do not create a separate ideas directory.

## Default Flow

Use this path for harness initialization, greenfield projects, and short feature ideas.

1. Restate the idea as a clear problem statement.
2. Ask at most 3 clarifying questions if target user, success criteria, or constraints are unclear.
3. Identify the target user, desired outcome, constraints, and key assumptions.
4. Propose 1 recommended direction and, only if useful, 1-2 alternatives.
5. Define the smallest MVP that tests the core assumption.
6. Make the `Not Doing` list explicit.
7. Ask the user to confirm before saving `idea.md` or moving to spec.

Do not run a full brainstorming workshop by default. The goal is a buildable brief, not a large idea catalogue.

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

## Recommended Direction
[The chosen direction and why. Keep this to 1-2 short paragraphs.]

## Constraints
- [Time, tech, budget, platform, compliance, or project constraints.]

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
- Do not silently choose a technology stack; record it as an assumption or open question if unclear.
- Do not turn the idea brief into an implementation plan. Planning belongs in `plan.md`.
- Do not over-expand a simple idea. Prefer the shortest useful path to a spec.
- If inside an existing codebase, ground assumptions in repository evidence when available.

## Verification

Before handing off to spec:

- [ ] Problem statement is clear.
- [ ] Target user is specific.
- [ ] Success criteria are testable.
- [ ] MVP scope is small enough to build first.
- [ ] Key assumptions and non-goals are explicit.
- [ ] User confirmed the direction or unresolved questions are recorded.

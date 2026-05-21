# Related Skills

Use this reference when operating `agent-harness` with other skills.

## idea-refine

Layer: Idea / Discovery

Status: bundled dependency

Use when:

- A request starts as a raw idea, product concept, or vague feature direction.
- The target user, value proposition, success criteria, or MVP scope is unclear.
- The team needs to explore multiple directions before committing to a spec.

Expected harness outputs:

- `harness/runs/<run>/idea.md`
- Clear problem statement, recommended direction, assumptions to validate, MVP scope, not-doing list, and open questions.

Do not use it for narrow bug fixes or already-approved implementation specs.

## spec-driven-development

Layer: Spec

Status: bundled dependency

Use when:

- A task is ambiguous, multi-file, or likely to take more than 30 minutes.
- The user wants a project, feature, or significant change.
- The definition of done is not already explicit.

Expected harness outputs:

- `harness/runs/<run>/spec.md`
- Clear goal, scope, non-goals, success criteria, acceptance criteria, required evidence, verification commands, and open questions.

## task-planning

Layer: Plan / Tasks

Status: bundled dependency

Use when:

- A validated spec needs implementation sequencing.
- Work needs to be split into small, verifiable tasks.
- Parallel work or checkpoints may be useful.

Expected harness outputs:

- `harness/runs/<run>/plan.md`
- Ordered tasks with dependencies, acceptance criteria, required evidence, verification steps, likely files, and checkpoints.

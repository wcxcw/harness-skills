# Related Workflow Skills

Use this reference when operating `agent-harness` with the bundled closed-loop workflows.

## brainstorming

Layer: Intake / Design

Expected output:

- `harness/runs/<run>/workflow.md`
- `harness/runs/<run>/design.md`

Use when a request starts as a raw idea, product concept, or vague feature direction.

## writing-specs

Layer: Spec

Expected output:

- `harness/runs/<run>/spec.md`

Use when the definition of done, scope, acceptance criteria, or required evidence is not explicit.

## writing-plans

Layer: Plan

Expected output:

- `harness/runs/<run>/plan.md`

Use when an accepted spec needs implementation sequencing.

## executing-plans

Layer: Execute

Expected output:

- `harness/runs/<run>/execution-log.md`

Use after the before-implementation gate passes.

## test-driven-development

Layer: Execute / Verification

Expected output:

- Focused failing test, implementation, passing test result, and evidence in `execution-log.md`

Use when behavior can be validated with automated tests.

## systematic-debugging

Layer: Debugging

Expected output:

- Reproduction, suspected cause, fix evidence, and regression proof in `execution-log.md`

Use for bug reports, regressions, or unexplained failures.

## requesting-code-review

Layer: Review

Expected output:

- `harness/runs/<run>/review.md`

Use after implementation and before completion.

## verification-before-completion

Layer: Verify

Expected output:

- Updated `execution-log.md`
- Passing completion gate or recorded reason it cannot run

Use before claiming completion.

## finishing-run

Layer: Finish / Evaluate

Expected output:

- `harness/runs/<run>/evaluation.md`

Use to close the run with acceptance status, residual risk, and harness feedback.

## writing-skills

Layer: Meta / Harness Improvement

Expected output:

- Updated skill or skill proposal, with attribution and verification

Use when creating, merging, or improving workflow skills.

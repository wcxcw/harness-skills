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

## context-budget

Layer: Context Control

Expected output:

- Context choices recorded in `workflow.md`, `execution-log.md`, or `evaluation.md` when they affect the run

Use when the project has multiple context files, long run history, or a task risks loading more context than it needs.

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

## code-reviewer

Layer: Review / Dedicated Reviewer Role

Expected output:

- Independent findings in `review.md`

Use as a subagent reviewer when the platform supports subagents, or as a focused local review checklist otherwise.

## code-quality-review

Layer: Review / Maintainability

Expected output:

- Code-quality findings and resolution in `review.md`
- Follow-up verification in `execution-log.md`

Use for application code changes before final verification.

## frontend-quality-review

Layer: Review / Frontend Quality

Expected output:

- Frontend maintainability, accessibility, responsive, and browser evidence in `review.md` and `execution-log.md`

Use for UI, frontend, browser, or client-side application changes.

## backend-quality-review

Layer: Review / Backend Quality

Expected output:

- Backend boundary, logging, error-handling, and operability findings in `review.md`

Use for backend, API, service, worker, persistence, CLI, or integration changes.

## receiving-code-review

Layer: Review Resolution

Expected output:

- Updated `review.md` resolution
- Updated `execution-log.md` verification evidence
- Updated `evaluation.md` residual risk when needed

Use when review feedback requires fixes, clarification, pushback, or accepted residual risk.

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

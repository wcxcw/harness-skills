# Skill Compatibility

This project harness is the source of truth for project facts, gates, commands, and completion evidence. Workflow skills may be used as helpers, but they do not replace local harness gates.

## Stage Mapping

| Harness stage | Required workflow skill | Compatible external skill pattern |
| --- | --- | --- |
| Intake | `brainstorming` | brainstorming |
| Spec | `writing-specs` | planning-oriented discovery |
| Plan | `writing-plans` | writing-plans |
| Preflight | `agent-harness` | local gate check |
| Implementation | `executing-plans` | test-driven-development when practical |
| Debugging | `systematic-debugging` | systematic-debugging |
| Review | `requesting-code-review` | requesting-code-review |
| Completion | `verification-before-completion`, `finishing-run` | verification-before-completion |
| Harness improvement | `writing-skills` | writing-skills when improving skills |

## Rules

- Use external skills only when they help satisfy the local spec, plan, gate, or verification requirement.
- Do not treat an external skill as approval to bypass `harness/controls/gates.md`.
- Record the skill or workflow used in `workflow.md`.
- If an external skill conflicts with project commands, guardrails, or user instructions, follow the local harness and ask when the conflict is material.

## Recommended Run Note

Add a short note to `workflow.md`:

```text
## Skills Used
- brainstorming
- writing-specs
- writing-plans

## Gates
- before-implementation: pending
- before-completion: pending
```

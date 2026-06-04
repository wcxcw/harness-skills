---
name: test-driven-development
description: Use a test-first loop for implementation tasks where behavior can be verified with automated tests.
---

# Test-Driven Development

Use this skill when implementing logic, bug fixes, APIs, parsers, transformations, or other behavior that can be tested.

## Gate Contract

- Owns RED/GREEN/REFACTOR evidence inside `execution-log.md`.
- TDD evidence helps satisfy `check_run.py --stage before-completion`, but it does not replace review or evaluation artifacts required by the selected tier.
- If TDD is not applicable, record the reason and the substitute verification in `execution-log.md`.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | TDD evidence when behavior changed and tests exist | Supports completion evidence |
| `standard` | RED/GREEN command evidence in `execution-log.md` | Supports `check_run.py --stage before-completion` |
| `full` | RED/GREEN/REFACTOR evidence plus broader verification | Supports review and final verification |

## Loop

1. RED: write or update one focused test for one target behavior.
2. Verify RED: run the narrow test and record the expected failure in `execution-log.md`.
3. GREEN: implement the smallest change that satisfies the test.
4. Verify GREEN: re-run the narrow test and record the passing result.
5. REFACTOR: clean up only after the test is green.
6. Re-run the narrow test after refactor.
7. Run broader relevant verification from `plan.md` or `harness/tools/commands.md`.
8. Record all command evidence in `execution-log.md`.

Do not use TDD as a reason to expand scope. For UI-only, documentation, or exploratory work, record why TDD is not applicable.

## Evidence Format

```markdown
## TDD: [behavior]

- RED command: `[command]`
- RED result: failed as expected because [specific reason]
- GREEN command: `[command]`
- GREEN result: passed
- REFACTOR command: `[command or "None"]`
- Broader verification: `[command/manual check]`
```

If the RED test passes immediately, the test is not proving new behavior. Rewrite it or document that the behavior already exists and adjust the plan.

## Stop Conditions

- No failing test was observed for new behavior that can be automated.
- The RED failure is caused by a typo, bad setup, or wrong assertion rather than missing behavior.
- GREEN requires broad unrelated changes.
- Refactor changes behavior or makes the narrow test fail.

## Evidence Examples

```markdown
## TDD: standard tier rejects missing plan

- RED command: `python3 -m unittest tests/test_agent_harness_scaffold.py`
- RED result: failed as expected because missing `plan.md` was not rejected
- GREEN command: `python3 -m unittest tests/test_agent_harness_scaffold.py`
- GREEN result: passed
- REFACTOR command: `python3 -m unittest tests/test_agent_harness_scaffold.py`
- Broader verification: `git diff --check`
```

## Anti-Patterns

- Writing implementation first and tests afterward.
- Keeping code written before RED as "reference".
- Testing mocks instead of behavior when real code is practical.
- Expanding scope during GREEN.

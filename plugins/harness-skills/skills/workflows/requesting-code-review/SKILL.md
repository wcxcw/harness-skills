---
name: requesting-code-review
description: Review completed changes before final verification and record findings in `review.md`.
---

# Requesting Code Review

Use this skill after implementation and before final completion. This skill is the review coordinator: it decides whether review is needed, prepares the review scope, routes to the right reviewer role or quality dimension, and ensures findings are recorded and resolved.

Without an active run, review the relevant diff and request directly, then report findings and verification without creating run artifacts solely for review. Apply the run-specific procedure below only when a run exists.

## Gate Contract

- Owns `review.md` for `full` tier runs and any run with meaningful implementation risk.
- `full` tier runs require `review.md` before `check_run.py --stage before-completion` can pass.
- The coordinator assembles review contributions into the complete semantic schema below.
- Review findings must be fixed or explicitly accepted as residual risk before final verification.

## Gate Mapping

| Tier | Required output | Gate effect |
| --- | --- | --- |
| `xs` | Usually skipped; document reason in `evaluation.md` when skipped | No review artifact gate |
| `standard` | `review.md` when risk justifies it | Review gaps become residual risk |
| `full` | `review.md` with findings and resolution | Required before `check_run.py --stage before-completion` can pass |

## Review Routing

Do not run every review skill mechanically. Choose the smallest review path that covers the changed surface and risk.

| Change type | Review path |
| --- | --- |
| No-run micro change | Usually skip review; run the targeted check and summarize the result |
| Documentation/config only | Usually skip review unless the change affects commands, gates, CI, or policy |
| Small application code change | `code-quality-review` when maintainability, comments, logging, or tests could be affected |
| Frontend/UI/browser change | `code-reviewer` plus `frontend-quality-review` when UI, state, routing, accessibility, or browser behavior changed |
| Backend/API/service/data change | `code-reviewer` plus `backend-quality-review` when handlers, services, data, errors, logs, or external calls changed |
| Full/high-risk run | `code-reviewer` plus all applicable quality reviews |
| Review feedback or reviewer findings | `receiving-code-review`; keep fixes in the same active run |

Use `code-reviewer` as a focused review checklist when appropriate. Record whether the review was independent or self-review; do not describe self-review as independent. The local checker verifies required review structure, not reviewer independence or the quality of review.

## Output

Save review results to:

```text
harness/runs/YYYY-MM-DD-short-task-name/review.md
```

## Required Sections

Use these semantic sections in this order. The local checker accepts the canonical
English and Chinese headings; do not add a duplicate `## Review` sentinel.

```markdown
# Review

## Review Scope

## Findings

## Resolution

## Residual Risk
```

For a Chinese run:

```markdown
# Review

## Review 范围

## 发现

## 处理结果

## 剩余风险
```

## Review Procedure

1. Identify the review base from the user request, relevant diff, and any `spec.md` or `plan.md` required by the tier.
2. Set the run phase to `reviewing` with `check_run.py <run> --tier <tier> --set-phase reviewing`.
3. Classify the changed surface and risk using `Review Routing` and `harness/controls/risk-matrix.md` when present.
4. Use `code-reviewer/SKILL.md` as a focused review checklist when applicable. Treat reviewer findings as a contribution, not a complete `review.md`.
5. Add only the applicable quality review dimensions: `code-quality-review`, `frontend-quality-review`, and/or `backend-quality-review`.
6. Review the change as a fresh reader. Do not rely on implementation intent.
7. Prioritize correctness, regressions, missing tests, security, data loss, concurrency, accessibility, maintainability, logging/observability, and scope creep.
8. Record findings by severity with file and line when possible.
9. Fix Critical and Important findings before continuing, or record why the user accepted the risk.
10. Assemble or update all four required semantic sections in `review.md`; record the review method and resolve findings.
11. Re-run relevant verification and append evidence to `execution-log.md`.
12. Draft `evaluation.md` before the completion gate. Run `check_run.py --stage before-completion` during final verification, after the draft and required evidence exist.

If no findings exist, state that explicitly and record remaining test gaps.

## Finding Format

```markdown
- Severity: Critical | Important | Minor
- Location: `path/to/file:line`
- Issue: [behavioral risk]
- Required action: [fix, test, or accepted risk]
- Resolution: fixed | accepted | deferred
```

## Stop Conditions

- The diff, requirements, or verification evidence is not available.
- Critical or Important findings are unresolved and not explicitly accepted by the user.
- Review scope excludes changed behavior that affects acceptance criteria.
- The reviewer cannot map changes back to the user request or applicable `spec.md` and `plan.md`.

## Evidence Examples

```markdown
## Findings
- Severity: Important
- Location: `harness/scripts/check_run.py:82`
- Issue: `standard` tier does not reject unresolved `Needs decision`.
- Required action: add marker check and regression test.
- Resolution: fixed
```

## Anti-Patterns

- Reviewing only style when behavior changed.
- Running every review skill for every task instead of routing by surface and risk.
- Accepting "no findings" without checking tests and acceptance criteria.
- Writing raw reviewer notes directly to `review.md` without assembling all required semantic sections.
- Adding a meaningless `## Review` heading solely to satisfy a checker.
- Treating review as final verification.
- Deferring important findings without recording residual risk.

---
name: writing-skills
description: Create or improve workflow skills with clear triggers, outputs, gates, and verification.
---

# Writing Skills

Use this skill when creating, merging, or improving skills in this repository.

## Gate Contract

- Skill changes must preserve local Harness artifacts and `check_run.py` gates.
- When a skill affects generated scaffold behavior, add or update tests before claiming completion.
- If a workflow skill is changed, verify it still points to local artifacts such as `workflow.md`, `spec.md`, `plan.md`, `execution-log.md`, `review.md`, and `evaluation.md`.

## Rules

- Define the trigger and non-trigger clearly.
- Name the artifact the skill owns.
- Keep local harness gates authoritative.
- Include output language behavior.
- Include verification criteria.
- Add or update tests when the skill changes generated harness behavior.

For workflow skills with third-party inspiration, preserve attribution in `skills/workflows/NOTICE.md` and adapt the workflow to local run artifacts instead of copying upstream text blindly.

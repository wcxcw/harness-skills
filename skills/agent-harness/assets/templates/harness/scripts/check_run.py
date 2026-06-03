#!/usr/bin/env python3
"""Check an Agent Harness run directory against project-local gates."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTION_ALIASES = {
    "objective": ["Objective", "Goal", "目标"],
    "scope": ["In Scope", "Scope", "范围内", "范围"],
    "non_goals": ["Out of Scope", "Non-goals", "Non Goals", "范围外", "非目标", "明确不做"],
    "acceptance": ["Acceptance Criteria", "验收标准"],
    "verification": ["Verification", "验证"],
    "open_questions": ["Open Questions", "待确认问题", "开放问题"],
    "tasks": ["Tasks", "任务"],
    "skills_used": ["Skills Used", "使用的 Skills", "使用的 Skill"],
    "gates": ["Gates", "门槛"],
    "review": ["Review", "Code Review", "Review 结果", "代码 Review"],
}

BLOCKING_MARKERS = [
    "Needs decision",
    "需要决策",
    "TBD",
    "[TODO]",
    "TODO:",
]

EVIDENCE_MARKERS = [
    "command",
    "manual",
    "passed",
    "failed",
    "skipped",
    "命令",
    "手动",
    "通过",
    "失败",
    "跳过",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_section(text: str, aliases: list[str]) -> bool:
    for alias in aliases:
        pattern = rf"^##+\s+{re.escape(alias)}\s*$"
        if re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE):
            return True
    return False


def missing_sections(text: str, names: list[str]) -> list[str]:
    return [name for name in names if not has_section(text, SECTION_ALIASES[name])]


def contains_blocking_marker(text: str) -> list[str]:
    found = []
    for marker in BLOCKING_MARKERS:
        if marker.lower() in text.lower():
            found.append(marker)
    return found


def has_evidence(text: str) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in EVIDENCE_MARKERS)


def check_before_implementation(run_dir: Path, tier: str) -> list[str]:
    errors: list[str] = []
    workflow = run_dir / "workflow.md"
    design = run_dir / "design.md"
    spec = run_dir / "spec.md"
    plan = run_dir / "plan.md"

    if tier == "xs":
        existing_text = "\n".join(read(path) for path in [workflow, spec, plan] if path.exists())
        for marker in contains_blocking_marker(existing_text):
            errors.append(f"Blocking marker is still present: {marker}.")
        return errors

    if not workflow.exists():
        errors.append("Missing workflow.md.")
    if tier == "full" and not design.exists():
        errors.append("Missing design.md.")
    if not spec.exists():
        errors.append("Missing spec.md.")
    if not plan.exists():
        errors.append("Missing plan.md.")
    if errors:
        return errors

    spec_text = read(spec)
    plan_text = read(plan)
    workflow_text = read(workflow)
    for section in missing_sections(workflow_text, ["skills_used", "gates"]):
        errors.append(f"workflow.md is missing required section: {section}.")
    for section in missing_sections(
        spec_text,
        ["objective", "scope", "non_goals", "acceptance", "verification", "open_questions"],
    ):
        errors.append(f"spec.md is missing required section: {section}.")
    for section in missing_sections(plan_text, ["tasks", "verification"]):
        errors.append(f"plan.md is missing required section: {section}.")

    for marker in contains_blocking_marker(workflow_text + "\n" + spec_text + "\n" + plan_text):
        errors.append(f"Blocking marker is still present: {marker}.")

    return errors


def check_before_completion(run_dir: Path, tier: str) -> list[str]:
    errors: list[str] = []
    execution_log = run_dir / "execution-log.md"
    review = run_dir / "review.md"
    evaluation = run_dir / "evaluation.md"

    if not execution_log.exists():
        errors.append("Missing execution-log.md.")
    if tier == "full" and not review.exists():
        errors.append("Missing review.md.")
    if not evaluation.exists():
        errors.append("Missing evaluation.md.")
    if errors:
        return errors

    execution_text = read(execution_log)
    evaluation_text = read(evaluation)
    if not execution_text.strip():
        errors.append("execution-log.md is empty.")
    if not has_evidence(execution_text):
        errors.append("execution-log.md does not appear to record command or manual verification evidence.")
    if tier == "full":
        review_text = read(review)
        if not review_text.strip():
            errors.append("review.md is empty.")
        if not has_section(review_text, SECTION_ALIASES["review"]):
            errors.append("review.md is missing required section: review.")
    if not evaluation_text.strip():
        errors.append("evaluation.md is empty.")
    if not has_evidence(evaluation_text):
        errors.append("evaluation.md does not appear to record acceptance, verification, or risk evidence.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check an Agent Harness run directory.")
    parser.add_argument("run_dir", help="Path to harness/runs/<run>.")
    parser.add_argument(
        "--stage",
        choices=["before-implementation", "before-completion", "all"],
        default="all",
        help="Gate stage to check.",
    )
    parser.add_argument(
        "--tier",
        choices=["xs", "standard", "full"],
        default="standard",
        help="Run tier. xs requires minimal evidence; standard requires workflow/spec/plan; full also requires design and review.",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if args.stage in {"before-implementation", "all"}:
        errors.extend(check_before_implementation(run_dir, args.tier))
    if args.stage in {"before-completion", "all"}:
        errors.extend(check_before_completion(run_dir, args.tier))

    if errors:
        print("Harness gate failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Harness gate passed: {run_dir} ({args.stage})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

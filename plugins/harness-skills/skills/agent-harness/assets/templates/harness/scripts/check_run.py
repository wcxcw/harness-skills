#!/usr/bin/env python3
"""Check an Agent Harness run directory against project-local gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SECTION_ALIASES = {
    "alignment": ["Alignment", "需求共识", "对齐确认"],
    "objective": ["Objective", "Goal", "目标"],
    "scope": ["In Scope", "Scope", "范围内", "范围"],
    "non_goals": ["Out of Scope", "Non-goals", "Non Goals", "范围外", "非目标", "明确不做"],
    "acceptance": ["Acceptance Criteria", "验收标准"],
    "verification": ["Verification", "验证"],
    "open_questions": ["Open Questions", "待确认问题", "开放问题"],
    "tasks": ["Tasks", "任务"],
    "skills_used": ["Skills Used", "使用的 Skills", "使用的 Skill"],
    "gates": ["Gates", "门槛"],
    "review_scope": ["Review Scope", "Review 范围", "评审范围", "审查范围"],
    "findings": ["Findings", "Review Findings", "发现", "评审发现", "审查发现"],
    "resolution": ["Resolution", "Resolutions", "处理结果", "解决情况", "处置结果"],
    "residual_risk": ["Residual Risk", "Residual Risks", "剩余风险", "残余风险"],
}

BLOCKING_MARKERS = [
    "Needs decision",
    "需要决策",
    "TBD",
    "[TODO]",
    "TODO:",
]

ALIGNMENT_CONFIRMATION_PATTERNS = [
    r"^\s*-\s*Confirmed by user\s*:\s*(?:yes|true)\s*$",
    r"^\s*-\s*用户已确认\s*[：:]\s*(?:是|已确认|true)\s*$",
]

RUN_PHASES = ("active", "reviewing", "verifying", "closed")
SESSION_ENV_KEYS = ("CODEX_THREAD_ID", "CLAUDE_SESSION_ID")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def current_session_id() -> str | None:
    for key in SESSION_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            return value
    return None


def session_hash(session_id: str) -> str:
    return hashlib.sha256(session_id.encode("utf-8")).hexdigest()


def set_run_phase(run_dir: Path, tier: str, phase: str) -> str | None:
    state_path = run_dir / "run-state.json"
    previous = {}
    try:
        if state_path.exists():
            previous = json.loads(state_path.read_text(encoding="utf-8"))
            if not isinstance(previous, dict):
                previous = {}
    except (OSError, json.JSONDecodeError):
        previous = {}
    state = {
        "schema_version": 1,
        "run": run_dir.name,
        "tier": tier,
        "status": phase,
    }
    # The first active transition captures HEAD before implementation. Preserve it
    # through reviewing, verifying, and explicit closure, including resumptions.
    if isinstance(previous.get("git_base"), str):
        state["git_base"] = previous["git_base"]
    elif phase == "active":
        project = run_dir.resolve().parent.parent.parent
        try:
            git = subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD"], cwd=project,
                capture_output=True, text=True, timeout=5, check=False,
            )
            if git.returncode == 0 and git.stdout.strip():
                state["git_base"] = git.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    if phase != "closed":
        session_id = current_session_id()
        if session_id is None:
            return "No session ID is available; expected CODEX_THREAD_ID or CLAUDE_SESSION_ID."
        state["session_hash"] = session_hash(session_id)

    temporary = run_dir / ".run-state.json.tmp"
    try:
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(state_path)
    except OSError as exc:
        return f"Could not update run state: {exc}"
    return None


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
        # A decision marker must begin an item, not merely be mentioned in a
        # task such as "Fix the TODO: comment in foo.py".
        pattern = rf"^[ \t]*(?:[-*][ \t]*)?(?:\[ \][ \t]*)?{re.escape(marker)}(?=$|[ \t：:])"
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            found.append(marker)
    return found


def has_field(text: str, names: str) -> bool:
    """Recognize a labelled nonempty field or a populated Markdown section.

    This is a structural check, not a judgment of correctness or test success.
    """
    pattern = rf"^[ \t]*(?:[-*][ \t]*)?(?:\*\*)?(?:{names})(?:\*\*)?[ \t]*[：:][ \t]*(\S.*)$"
    if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
        return True
    nested = rf"^[ \t]*(?:[-*]\s*)?(?:\*\*)?(?:{names})(?:\*\*)?[ \t]*[：:][ \t]*\n[ \t]+(?:[-*][ \t]*)?\S.*$"
    if re.search(nested, text, re.IGNORECASE | re.MULTILINE):
        return True
    heading = re.search(rf"^##+\s+(?:{names})\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not heading:
        return False
    body = text[heading.end():]
    next_heading = re.search(r"^##+\s+", body, re.MULTILINE)
    return bool((body[:next_heading.start()] if next_heading else body).strip())


def has_inline_verification_result(text: str) -> bool:
    """Accept concise records such as `- 命令：...；通过。`."""
    label = r"(?:(?:red|green|refactor|final)\s+)?(?:commands?|manual(?:\s+checks?)?)|命令|手动(?:检查|验证)?"
    result = r"(?:passed|failed|skipped)\b|通过|失败|跳过"
    pattern = rf"^[ \t]*(?:[-*][ \t]*)?(?:{label})[ \t]*[：:][ \t]*\S[^\n]*?(?:[；;，,]|=>)[ \t]*(?:结果[：:]\s*)?(?:{result})"
    return bool(re.search(pattern, text, re.IGNORECASE | re.MULTILINE))


def section_body(text: str, aliases: list[str]) -> str | None:
    for alias in aliases:
        heading = re.search(
            rf"^##+\s+{re.escape(alias)}\s*$",
            text,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        if not heading:
            continue
        next_heading = re.search(r"^##+\s+", text[heading.end() :], flags=re.MULTILINE)
        end = heading.end() + next_heading.start() if next_heading else len(text)
        return text[heading.end() : end]
    return None


def has_confirmed_alignment(text: str) -> bool:
    alignment = section_body(text, SECTION_ALIASES["alignment"])
    if alignment is None:
        return False
    return any(
        re.search(pattern, alignment, flags=re.MULTILINE | re.IGNORECASE)
        for pattern in ALIGNMENT_CONFIRMATION_PATTERNS
    )


def check_before_implementation(run_dir: Path, tier: str) -> list[str]:
    errors: list[str] = []
    workflow = run_dir / "workflow.md"
    spec = run_dir / "spec.md"
    plan = run_dir / "plan.md"

    if tier == "xs":
        existing_text = "\n".join(read(path) for path in [workflow, spec, plan] if path.exists())
        for marker in contains_blocking_marker(existing_text):
            errors.append(f"Blocking marker is still present: {marker}.")
        return errors

    if not workflow.exists():
        errors.append("Missing workflow.md.")
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
        ["alignment", "objective", "scope", "non_goals", "acceptance", "verification", "open_questions"],
    ):
        errors.append(f"spec.md is missing required section: {section}.")
    if not has_confirmed_alignment(spec_text):
        errors.append("spec.md does not record user-confirmed alignment.")
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
    if not has_field(execution_text, r"(?:(?:red|green|refactor|final)\s+)?(?:commands?|manual(?:\s+checks?)?)|命令|手动(?:检查|验证)?"):
        errors.append("execution-log.md needs a labelled command or manual check with details.")
    if not has_field(execution_text, r"(?:(?:red|green|refactor|final)\s+)?(?:result|outcome)|结果|验证结果|检查结果") and not has_inline_verification_result(execution_text):
        errors.append("execution-log.md needs a labelled verification result with details.")
    if tier == "full":
        review_text = read(review)
        if not review_text.strip():
            errors.append("review.md is empty.")
        for section in missing_sections(
            review_text,
            ["review_scope", "findings", "resolution", "residual_risk"],
        ):
            errors.append(f"review.md is missing required section: {section}.")
    if not evaluation_text.strip():
        errors.append("evaluation.md is empty.")
    if not has_field(evaluation_text, r"acceptance(?:\s+status)?|verification(?:\s+(?:status|results?))?|risk|residual\s+risks?|验收(?:状态|结果|情况)?|验证(?:状态|结果|情况)?|风险|剩余风险|残余风险"):
        errors.append("evaluation.md needs a labelled acceptance, verification, or risk summary.")

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
        help="Run tier. xs requires minimal evidence; standard requires workflow/spec/plan; full also requires review.",
    )
    parser.add_argument(
        "--set-phase",
        choices=RUN_PHASES,
        help="Record the current session's run phase without executing a gate.",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}", file=sys.stderr)
        return 1

    if args.set_phase:
        error = set_run_phase(run_dir, args.tier, args.set_phase)
        if error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"Harness run phase set: {run_dir} ({args.tier}, {args.set_phase})")
        return 0

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

    print(f"Harness gate passed: {run_dir} ({args.stage}); structure checked, evidence and results still require review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

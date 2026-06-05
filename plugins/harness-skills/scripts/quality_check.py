#!/usr/bin/env python3
"""Lightweight Harness code-quality checks."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CODE_EXTENSIONS = {
    ".vue",
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".py",
    ".go",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".cs",
    ".rs",
}

FRONTEND_EXTENSIONS = {".vue", ".tsx", ".ts", ".jsx", ".js"}
BACKEND_HINTS = re.compile(r"(api|server|route|controller|service|worker|job|repository|dao|handler)", re.I)
SIDE_EFFECT_HINTS = re.compile(
    r"\b(fetch|axios|requests|httpx|prisma|sequelize|typeorm|sql|insert|update|delete|create|save|transaction|publish|enqueue)\b",
    re.I,
)
LOG_HINTS = re.compile(r"\b(log|logger|logging|tracer|trace|span|metrics|telemetry)\b", re.I)


@dataclass
class Finding:
    severity: str
    location: str
    issue: str
    action: str


def run_git(root: Path, args: list[str]) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            text=True,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def changed_files(root: Path) -> list[Path]:
    names = set(run_git(root, ["diff", "--name-only", "HEAD"]))
    names.update(run_git(root, ["diff", "--name-only", "--cached"]))
    return [
        root / name
        for name in sorted(names)
        if (root / name).is_file() and (root / name).suffix in CODE_EXTENSIONS
    ]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def is_frontend(path: Path) -> bool:
    return path.suffix in FRONTEND_EXTENSIONS and (
        path.name in {"App.vue", "App.tsx", "App.jsx", "App.ts", "App.js"}
        or any(part in {"src", "app", "pages", "components", "views", "routes"} for part in path.parts)
    )


def is_backend(path: Path) -> bool:
    rel = "/".join(path.parts).lower()
    return bool(BACKEND_HINTS.search(rel)) or path.suffix in {".py", ".go", ".java", ".kt", ".rb", ".php", ".cs", ".rs"}


def review_resolution_ok(block: str) -> bool:
    lowered = block.lower()
    return "resolution: fixed" in lowered or "resolution: accepted" in lowered or "accepted risk" in lowered or "用户明确接受" in lowered


def unresolved_review_findings(run_dir: Path | None) -> list[Finding]:
    if run_dir is None:
        return []
    review = run_dir / "review.md"
    if not review.exists():
        return []
    text = read_text(review)
    findings: list[Finding] = []
    matches = list(re.finditer(r"Severity:\s*(Critical|Important)", text, flags=re.I))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start() : end]
        if not review_resolution_ok(block):
            findings.append(
                Finding(
                    severity=match.group(1).capitalize(),
                    location=str(review),
                    issue="Review contains unresolved Critical or Important finding.",
                    action="Fix the finding, record `Resolution: fixed`, or record user-accepted residual risk.",
                )
            )
    return findings


def quality_review_missing(run_dir: Path | None, files: list[Path]) -> list[Finding]:
    if run_dir is None or not files:
        return []
    review = run_dir / "review.md"
    evaluation = run_dir / "evaluation.md"
    haystack = ""
    for path in (review, evaluation):
        if path.exists():
            haystack += "\n" + read_text(path)
    lowered = haystack.lower()
    has_review = any(
        marker in lowered
        for marker in (
            "code quality review",
            "frontend quality review",
            "backend quality review",
            "code-quality review",
            "代码质量 review",
            "质量 review",
        )
    )
    has_skip = "skip" in lowered and ("quality" in lowered or "review" in lowered)
    if has_review or has_skip:
        return []
    return [
        Finding(
            severity="Important",
            location=str(run_dir),
            issue="Application code changed but no code-quality review or skip reason is recorded.",
            action="Run `code-quality-review` and frontend/backend review when applicable, or record why it is skipped.",
        )
    ]


def file_findings(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        text = read_text(path)
        rel = path.relative_to(root)
        lines = text.splitlines()
        if path.name in {"App.vue", "App.tsx", "App.jsx", "App.ts", "App.js"}:
            has_data_access = bool(re.search(r"\b(fetch|axios|useQuery|graphql|client\.)\b", text, re.I))
            has_state = bool(re.search(r"\b(ref|reactive|useState|useReducer|createStore|computed)\b", text))
            if len(lines) > 300 or (len(lines) > 180 and has_data_access and has_state):
                findings.append(
                    Finding(
                        severity="Important",
                        location=f"{rel}:1",
                        issue="Root app component appears to own too much feature logic.",
                        action="Move data access/stateful logic into composables/hooks/stores and extract focused components.",
                    )
                )
        if is_frontend(path) and len(lines) > 450:
            findings.append(
                Finding(
                    severity="Minor",
                    location=f"{rel}:1",
                    issue="Large frontend file may be hard to review and test.",
                    action="Check whether component, state, and data access responsibilities can be split.",
                )
            )
        if is_backend(path) and SIDE_EFFECT_HINTS.search(text) and not LOG_HINTS.search(text):
            findings.append(
                Finding(
                    severity="Important",
                    location=f"{rel}:1",
                    issue="Backend or integration path has side-effect/external-call hints but no logging or observability marker.",
                    action="Add safe diagnostic logging where operationally relevant, or record why logging is not applicable.",
                )
            )
        if re.search(r"\bTODO|FIXME|HACK\b", text):
            findings.append(
                Finding(
                    severity="Minor",
                    location=f"{rel}:1",
                    issue="Temporary marker remains in changed code.",
                    action="Resolve it or record why it is acceptable for this task.",
                )
            )
    return findings


def render_text(findings: list[Finding]) -> str:
    if not findings:
        return "Harness quality check passed."
    lines = ["Harness quality check failed:"]
    for finding in findings:
        lines.extend(
            [
                f"- Severity: {finding.severity}",
                f"  Location: {finding.location}",
                f"  Issue: {finding.issue}",
                f"  Required action: {finding.action}",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight Harness quality checks.")
    parser.add_argument("--project", default=".", help="Project root.")
    parser.add_argument("--run", help="Active harness run directory.")
    parser.add_argument("--strict", action="store_true", help="Fail on Important findings.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    run_dir = Path(args.run).resolve() if args.run else None
    files = changed_files(root)
    findings = []
    findings.extend(file_findings(root, files))
    findings.extend(unresolved_review_findings(run_dir))
    findings.extend(quality_review_missing(run_dir, files))

    if args.json:
        print(
            json.dumps(
                {"findings": [finding.__dict__ for finding in findings]},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_text(findings))

    blocking = {"Critical", "Important"} if args.strict else {"Critical"}
    return 1 if any(finding.severity in blocking for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

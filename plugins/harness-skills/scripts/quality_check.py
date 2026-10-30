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
TEMPORARY_COMMENT_HINTS = re.compile(
    r"(?:#|//|/\*+|\*|--|<!--)\s*(?:TODO|FIXME|HACK)\b",
    re.I,
)


@dataclass
class Finding:
    severity: str
    location: str
    issue: str
    action: str


def run_git(root: Path, args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            text=True,
            errors="surrogateescape",
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def changed_files(root: Path, run_dir: Path | None) -> tuple[list[Path], dict[Path, str], str | None]:
    if run_git(root, ["rev-parse", "--show-toplevel"]) is None:
        return [], {}, "Git change detection is unavailable; code files were not scanned."
    baseline = None
    state_path = run_dir / "run-state.json" if run_dir else None
    if state_path and state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            candidate = state.get("git_base") if isinstance(state, dict) else None
            if isinstance(candidate, str) and re.fullmatch(r"[0-9a-f]{40,64}", candidate):
                baseline = candidate
        except (OSError, json.JSONDecodeError):
            pass
    head = run_git(root, ["rev-parse", "--verify", "HEAD"])
    warning = None
    if baseline:
        diff = run_git(root, ["diff", "--no-renames", "--name-only", "-z", "--relative", baseline, "--"])
        if diff is None:
            return [], {}, "The run's Git baseline cannot be compared; code files were not scanned."
    elif head is not None:
        diff = run_git(root, ["diff", "--no-renames", "--name-only", "-z", "--relative", "HEAD", "--"])
        warning = "No run baseline is available; committed changes are not included."
    else:
        diff = run_git(root, ["diff", "--no-renames", "--name-only", "-z", "--cached", "--relative", "--"])
        warning = "No Git HEAD or run baseline is available; committed changes are not included."
    untracked = run_git(root, ["ls-files", "--others", "--exclude-standard", "-z", "--"])
    staged = run_git(root, ["diff", "--no-renames", "--cached", "--name-only", "-z", "--relative", "--"])
    working = run_git(root, ["diff", "--no-renames", "--name-only", "-z", "--relative", "--"])
    staged_base = run_git(root, ["diff", "--no-renames", "--cached", "--name-only", "-z", "--relative", baseline, "--"]) if baseline else staged
    if any(value is None for value in (diff, untracked, staged, working, staged_base)):
        return [], {}, "Git change detection failed; code files were not scanned."
    index_changed = set(staged.split("\0")) | set(staged_base.split("\0"))
    working_changed = set(working.split("\0"))
    names = set(diff.split("\0")) | set(untracked.split("\0")) | index_changed | working_changed
    staged_contents = {}
    # A separate index read is only useful when its content differs from the
    # working tree. Committed baseline changes otherwise need no git show.
    for name in sorted(working_changed & names):
        if not name or (root / name).suffix not in CODE_EXTENSIONS:
            continue
        # git show uses a project-relative index path, even when the project
        # sits in a subdirectory of the repository.
        content = run_git(root, ["show", f":./{name}"])
        if content is not None:
            staged_contents[root / name] = content
        elif (root / name).is_file():
            warning = (warning + " " if warning else "") + f"Staged content for {name} could not be read."
    files = [
        root / name
        for name in sorted(names)
        if name and (root / name).suffix in CODE_EXTENSIONS
    ]
    return files, staged_contents, warning


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
    return (
        bool(re.search(r"resolution\s*:\s*(?:fixed|accepted)\b", lowered))
        or bool(re.search(r"处理结果\s*[：:]\s*(?:fixed|accepted|已修复|已接受|已处理)", block, flags=re.I))
        or "accepted risk" in lowered
        or "用户明确接受" in lowered
    )


def unresolved_review_findings(run_dir: Path | None) -> list[Finding]:
    if run_dir is None:
        return []
    review = run_dir / "review.md"
    if not review.exists():
        return []
    text = read_text(review)
    findings: list[Finding] = []
    matches = list(
        re.finditer(
            r"(?:Severity|严重程度)\s*[：:]\s*(Critical|Important)",
            text,
            flags=re.I,
        )
    )
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


def file_findings(root: Path, files: list[Path], staged_contents: dict[Path, str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        worktree_text = read_text(path) if path.is_file() else None
        versions = [(worktree_text, "")] if worktree_text is not None else []
        staged_text = staged_contents.get(path)
        if staged_text is not None and staged_text != worktree_text:
            versions.append((staged_text, " (staged)"))
        for text, suffix in versions:
            findings.extend(file_version_findings(root, path, text, suffix))
    return findings


def file_version_findings(root: Path, path: Path, text: str, suffix: str) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(path.relative_to(root)) + suffix
    lines = text.splitlines()
    if path.name in {"App.vue", "App.tsx", "App.jsx", "App.ts", "App.js"}:
        has_data_access = bool(re.search(r"\b(fetch|axios|useQuery|graphql|client\.)\b", text, re.I))
        has_state = bool(re.search(r"\b(ref|reactive|useState|useReducer|createStore|computed)\b", text))
        if len(lines) > 300 or (len(lines) > 180 and has_data_access and has_state):
            findings.append(
                Finding(
                    severity="Minor",
                    location=f"{rel}:1",
                    issue="Root app component appears to own too much feature logic.",
                    action="Review whether responsibilities should be split; this heuristic is advisory.",
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
                severity="Minor",
                location=f"{rel}:1",
                issue="Backend or integration path has side-effect/external-call hints but no logging or observability marker.",
                action="Review whether safe diagnostic logging is appropriate; this heuristic is advisory.",
            )
        )
    if TEMPORARY_COMMENT_HINTS.search(text):
        findings.append(
            Finding(
                severity="Minor",
                location=f"{rel}:1",
                issue="Temporary marker remains in changed code.",
                action="Resolve it or record why it is acceptable for this task.",
            )
        )
    return findings


def render_text(findings: list[Finding], blocking: set[str]) -> str:
    if not findings:
        return "Harness quality check passed."
    status = "failed" if any(finding.severity in blocking for finding in findings) else "completed with warnings"
    lines = [f"Harness quality check {status}:"]
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
    files, staged_contents, scan_warning = changed_files(root, run_dir)
    findings = []
    if scan_warning:
        findings.append(Finding("Minor", str(root), scan_warning, "Review the missing coverage manually."))
    findings.extend(file_findings(root, files, staged_contents))
    findings.extend(unresolved_review_findings(run_dir))
    application_files = [path for path in files if path.relative_to(root).parts[:2] != ("harness", "scripts")]
    findings.extend(quality_review_missing(run_dir, application_files))

    blocking = {"Critical", "Important"} if args.strict else {"Critical"}
    if args.json:
        print(
            json.dumps(
                {"findings": [finding.__dict__ for finding in findings]},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_text(findings, blocking))

    return 1 if any(finding.severity in blocking for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

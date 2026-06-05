#!/usr/bin/env python3
"""Codex hook entry point for Harness Skills."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def project_root(payload: dict) -> Path:
    for key in ("cwd", "workspace_root", "workspaceRoot", "project_root", "projectRoot"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return Path(value).expanduser().resolve()
    return Path.cwd().resolve()


def latest_run(root: Path) -> Path | None:
    runs_dir = root / "harness" / "runs"
    if not runs_dir.is_dir():
        return None
    candidates = [
        path
        for path in runs_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    ]
    candidates = [
        path
        for path in candidates
        if any((path / name).exists() for name in ("execution-log.md", "evaluation.md", "spec.md", "plan.md"))
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def infer_tier(run_dir: Path) -> str:
    if (run_dir / "design.md").exists() and (run_dir / "review.md").exists():
        return "full"
    if (run_dir / "workflow.md").exists() and (run_dir / "spec.md").exists() and (run_dir / "plan.md").exists():
        return "standard"
    return "xs"


def run_command(command: list[str], cwd: Path) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return completed.returncode, output.strip()


def session_start() -> None:
    emit(
        {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": (
                    "Harness Skills hook active. For harness projects, read project-brief first, "
                    "avoid bulk-reading harness/context or completed runs, and run stop-time gates "
                    "before claiming completion."
                ),
            },
        }
    )


def stop(payload: dict) -> None:
    if payload.get("stop_hook_active"):
        emit({"continue": True})
        return

    root = project_root(payload)
    if not (root / "harness").is_dir():
        emit({"continue": True})
        return

    reasons: list[str] = []
    run_dir = latest_run(root)
    checker = root / "harness" / "scripts" / "check_run.py"
    if run_dir and checker.exists():
        tier = infer_tier(run_dir)
        code, output = run_command(
            [
                sys.executable,
                str(checker),
                str(run_dir),
                "--stage",
                "before-completion",
                "--tier",
                tier,
            ],
            root,
        )
        if code != 0:
            reasons.append(
                f"Harness completion gate failed for `{run_dir.relative_to(root)}` ({tier}).\n{output}"
            )

    plugin_root = Path(
        os.environ.get("CLAUDE_PLUGIN_ROOT")
        or os.environ.get("CODEX_PLUGIN_ROOT")
        or Path(__file__).resolve().parents[1]
    )
    quality_check = plugin_root / "scripts" / "quality_check.py"
    if quality_check.exists():
        command = [sys.executable, str(quality_check), "--project", str(root)]
        if run_dir:
            command += ["--run", str(run_dir), "--strict"]
        code, output = run_command(command, root)
        if code != 0:
            reasons.append(output or "Harness quality gate failed.")

    if reasons:
        emit(
            {
                "decision": "block",
                "reason": (
                    "Before final response, address the Harness gate result below. "
                    "Fix the issue, record verification evidence, or record user-accepted residual risk.\n\n"
                    + "\n\n".join(reasons)
                ),
            }
        )
        return

    emit({"continue": True})


def main() -> int:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = read_payload()
    if event == "SessionStart":
        session_start()
    elif event == "Stop":
        stop(payload)
    else:
        emit({"continue": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

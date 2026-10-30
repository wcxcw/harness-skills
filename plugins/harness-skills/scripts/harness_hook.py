#!/usr/bin/env python3
"""Codex hook entry point for Harness."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        return {}


def project_root(payload: dict) -> Path:
    for key in ("cwd", "workspace_root", "workspaceRoot", "project_root", "projectRoot"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return Path(value).expanduser().resolve()
    return Path.cwd().resolve()


SESSION_PAYLOAD_KEYS = ("session_id", "sessionId", "thread_id", "threadId", "conversation_id", "conversationId")
SESSION_ENV_KEYS = ("CODEX_THREAD_ID", "CLAUDE_SESSION_ID")
RUN_TIERS = {"xs", "standard", "full"}
# Stop has a 30-second host timeout. Keep time to report a useful failure.
STOP_BUDGET_SECONDS = 26.0
COMMAND_TIMEOUT_SECONDS = 12.0


def current_session_id(payload: dict) -> str | None:
    for key in SESSION_PAYLOAD_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    for key in SESSION_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            return value
    return None


def session_hash(session_id: str) -> str:
    return hashlib.sha256(session_id.encode("utf-8")).hexdigest()


def verifying_runs(root: Path, expected_session_hash: str) -> list[tuple[Path, str]]:
    runs_dir = root / "harness" / "runs"
    if not runs_dir.is_dir():
        return []
    matches: list[tuple[Path, str]] = []
    for run_dir in runs_dir.iterdir():
        state_path = run_dir / "run-state.json"
        if not run_dir.is_dir() or not state_path.exists():
            continue
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(state, dict):
            continue
        tier = state.get("tier")
        if (
            state.get("schema_version") == 1
            and state.get("run") == run_dir.name
            and state.get("status") == "verifying"
            and state.get("session_hash") == expected_session_hash
            and tier in RUN_TIERS
        ):
            matches.append((run_dir, tier))
    return sorted(matches, key=lambda item: item[0].name)


def close_run(run_dir: Path, tier: str) -> str | None:
    state_path = run_dir / "run-state.json"
    try:
        previous = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        previous = {}
    state = {
        "schema_version": 1,
        "run": run_dir.name,
        "tier": tier,
        "status": "closed",
    }
    if isinstance(previous, dict) and isinstance(previous.get("git_base"), str):
        state["git_base"] = previous["git_base"]
    temporary = run_dir / ".run-state.json.tmp"
    try:
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(state_path)
    except OSError as exc:
        return f"Could not close Harness run `{run_dir}`: {exc}"
    return None


def run_command(command: list[str], cwd: Path, timeout: float = COMMAND_TIMEOUT_SECONDS) -> tuple[int, str]:
    if timeout <= 0:
        return 1, "Harness Stop time budget exhausted before this check could run."
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout,
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
                    "Harness hook active. For harness projects, use project-brief for "
                    "first orientation or when context may be stale; reuse it within the same "
                    "session when already loaded. Avoid bulk-reading harness/context or completed "
                    "runs. Before creating a run for an unclear objective, invite the user to "
                    "explicitly invoke $grilling; it creates no files, and its confirmed result "
                    "feeds spec.md directly. Stop-time completion gates apply only to a run that "
                    "this session explicitly marks as verifying."
                ),
            },
        }
    )


def stop(payload: dict) -> None:
    deadline = time.monotonic() + STOP_BUDGET_SECONDS
    root = project_root(payload)
    if not (root / "harness").is_dir():
        emit({"continue": True})
        return

    session_id = current_session_id(payload)
    if session_id is None:
        emit({"continue": True})
        return

    reasons: list[str] = []
    warnings: list[str] = []
    runs = verifying_runs(root, session_hash(session_id))
    if not runs:
        emit({"continue": True})
        return

    checker = root / "harness" / "scripts" / "check_run.py"
    if not checker.exists():
        reasons.append("Harness completion gate cannot run because `harness/scripts/check_run.py` is missing.")
    plugin_root = Path(
        os.environ.get("CLAUDE_PLUGIN_ROOT")
        or os.environ.get("CODEX_PLUGIN_ROOT")
        or Path(__file__).resolve().parents[1]
    )
    quality_check = plugin_root / "scripts" / "quality_check.py"
    for run_dir, tier in runs:
        if checker.exists():
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
                timeout=min(COMMAND_TIMEOUT_SECONDS, deadline - time.monotonic()),
            )
            if code != 0:
                reasons.append(
                    f"Harness completion gate failed for `{run_dir.relative_to(root)}` ({tier}).\n{output}"
                )

        if quality_check.exists():
            command = [
                sys.executable,
                str(quality_check),
                "--project",
                str(root),
                "--run",
                str(run_dir),
                "--strict",
            ]
            code, output = run_command(command, root, timeout=min(COMMAND_TIMEOUT_SECONDS, deadline - time.monotonic()))
            if code != 0:
                reasons.append(output or "Harness quality gate failed.")
            elif output and output != "Harness quality check passed.":
                warnings.append(output)

    if not reasons:
        for run_dir, tier in runs:
            error = close_run(run_dir, tier)
            if error:
                reasons.append(error)

    if reasons:
        if payload.get("stop_hook_active"):
            # A failed retry must not start an endless Stop continuation loop.
            # Keep the run verifying and surface the unresolved failure.
            emit({"continue": True, "systemMessage": "Harness gate still failing; run remains verifying.\n" + "\n\n".join(reasons)})
            return
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

    if warnings:
        emit({"continue": True, "systemMessage": "\n\n".join(warnings)})
    else:
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

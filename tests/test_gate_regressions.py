from __future__ import annotations

import hashlib
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "harness-skills"
CHECKER = PLUGIN / "skills" / "agent-harness" / "assets" / "templates" / "harness" / "scripts" / "check_run.py"
QUALITY = PLUGIN / "scripts" / "quality_check.py"
HOOK = PLUGIN / "scripts" / "harness_hook.py"


class GateRegressionTest(unittest.TestCase):
    def test_closed_run_can_resume_in_another_session_and_close_again(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args: str) -> None:
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            (root / "notes.txt").write_text("initial\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            run = root / "harness" / "runs" / "test"
            run.mkdir(parents=True)
            checker = root / "harness" / "scripts" / "check_run.py"
            checker.parent.mkdir(parents=True)
            checker.write_bytes(CHECKER.read_bytes())
            (run / "execution-log.md").write_text("Command: check\nResult: passed\n", encoding="utf-8")
            (run / "evaluation.md").write_text("Acceptance: passed\n", encoding="utf-8")
            def phase(value: str, session: str) -> None:
                subprocess.run([sys.executable, str(checker), str(run), "--tier", "xs", "--set-phase", value], env={**os.environ, "CODEX_THREAD_ID": session}, check=True, capture_output=True)
            def state() -> dict:
                return json.loads((run / "run-state.json").read_text())
            def stop(session: str) -> dict:
                result = subprocess.run([sys.executable, str(HOOK), "Stop"], input=json.dumps({"cwd": str(root), "session_id": session}), capture_output=True, text=True, check=True, env={**os.environ, "CODEX_PLUGIN_ROOT": str(PLUGIN)})
                return json.loads(result.stdout)
            phase("active", "first")
            baseline = state()["git_base"]
            phase("closed", "first")
            (root / "notes.txt").write_text("updated\n", encoding="utf-8")
            git("add", "notes.txt")
            git("commit", "-qm", "updated")
            phase("active", "second")
            self.assertEqual(state()["git_base"], baseline)
            self.assertEqual(state()["session_hash"], hashlib.sha256(b"second").hexdigest())
            phase("verifying", "second")
            self.assertTrue(stop("first")["continue"])
            self.assertEqual(state()["status"], "verifying")
            self.assertTrue(stop("second")["continue"])
            self.assertEqual(state()["status"], "closed")
            self.assertEqual(state()["git_base"], baseline)

    def test_deleted_and_renamed_code_still_requires_application_review(self) -> None:
        for case in ("unstaged", "staged", "committed", "rename", "harness-only"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                def git(*args: str) -> None:
                    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
                git("init", "-q")
                git("config", "user.name", "Test")
                git("config", "user.email", "test@example.invalid")
                app = root / "app.py"
                app.write_text("value = 1\n", encoding="utf-8")
                script = root / "harness" / "scripts" / "check_run.py"
                script.parent.mkdir(parents=True)
                script.write_text("value = 1\n", encoding="utf-8")
                git("add", ".")
                git("commit", "-qm", "base")
                run = root / "harness" / "runs" / "test"
                run.mkdir(parents=True)
                subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--set-phase", "active"], env={**os.environ, "CODEX_THREAD_ID": "test"}, check=True, capture_output=True)
                if case == "unstaged":
                    app.unlink()
                elif case == "rename":
                    git("mv", "app.py", "notes.txt")
                elif case == "harness-only":
                    git("rm", "-q", "harness/scripts/check_run.py")
                else:
                    git("rm", "-q", "app.py")
                    if case == "committed":
                        git("commit", "-qm", "remove app")
                result = subprocess.run([sys.executable, str(QUALITY), "--project", str(root), "--run", str(run), "--json", "--strict"], capture_output=True, text=True)
                findings = json.loads(result.stdout)["findings"]
                missing_review = any("no code-quality review" in f["issue"] for f in findings)
                self.assertEqual(missing_review, case != "harness-only", result.stdout)
                self.assertEqual(result.returncode != 0, case != "harness-only", result.stdout)

    def test_staged_content_is_scanned_even_when_worktree_matches_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args: str) -> None:
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            source = root / "服务.py"
            source.write_text("value = 1\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            run = root / "harness" / "runs" / "test"
            run.mkdir(parents=True)
            subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--set-phase", "active"], env={**os.environ, "CODEX_THREAD_ID": "test"}, check=True, capture_output=True)
            source.write_text("# TODO staged bug\n", encoding="utf-8")
            git("add", "服务.py")
            source.write_text("value = 1\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(QUALITY), "--project", str(root), "--run", str(run), "--json", "--strict"], capture_output=True, text=True)
            findings = json.loads(result.stdout)["findings"]
            self.assertTrue(any(f["location"] == "服务.py (staged):1" and "Temporary marker" in f["issue"] for f in findings))
            self.assertTrue(any("no code-quality review" in f["issue"] for f in findings))

    def test_scaffold_code_and_large_app_advisories_do_not_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True)
            run = root / "harness" / "runs" / "test"
            run.mkdir(parents=True)
            script = root / "harness" / "scripts" / "check_run.py"
            script.parent.mkdir(parents=True)
            script.write_text("def create():\n    return 1\n", encoding="utf-8")
            def quality() -> subprocess.CompletedProcess:
                return subprocess.run([sys.executable, str(QUALITY), "--project", str(root), "--run", str(run), "--json", "--strict"], capture_output=True, text=True)
            result = quality()
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertFalse(any("no code-quality review" in f["issue"] for f in json.loads(result.stdout)["findings"]))
            (run / "evaluation.md").write_text("code quality review: passed\n", encoding="utf-8")
            app = root / "src" / "App.tsx"
            app.parent.mkdir()
            app.write_text("\n".join(f"// line {i}" for i in range(350)), encoding="utf-8")
            result = quality()
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertTrue(any(f["severity"] == "Minor" and "Root app component" in f["issue"] for f in json.loads(result.stdout)["findings"]))

    def test_stop_checks_share_a_bounded_time_budget(self) -> None:
        spec = importlib.util.spec_from_file_location("harness_hook_budget_test", HOOK)
        hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("first", "second"):
                run = root / "harness" / "runs" / name
                run.mkdir(parents=True)
                (run / "run-state.json").write_text(json.dumps({"schema_version": 1, "run": name, "tier": "xs", "status": "verifying", "session_hash": hashlib.sha256(b"test").hexdigest()}))
            checker = root / "harness" / "scripts" / "check_run.py"
            checker.parent.mkdir(parents=True)
            checker.write_text("import time\ntime.sleep(5)\n")
            out = io.StringIO()
            started = time.monotonic()
            with patch.object(hook, "STOP_BUDGET_SECONDS", 0.2), patch.dict(os.environ, {"CODEX_PLUGIN_ROOT": str(PLUGIN)}), contextlib.redirect_stdout(out):
                hook.stop({"cwd": str(root), "session_id": "test"})
            self.assertLess(time.monotonic() - started, 2)
            result = json.loads(out.getvalue())
            self.assertEqual(result["decision"], "block")
            self.assertIn("time budget exhausted", result["reason"])

    def test_scope_includes_committed_untracked_and_unicode_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args: str) -> None:
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            (root / "服务.py").write_text("value = 1\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            run = root / "harness" / "runs" / "test"
            run.mkdir(parents=True)
            env = {**os.environ, "CODEX_THREAD_ID": "test-session"}
            subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--set-phase", "active"], env=env, check=True, capture_output=True)
            baseline = json.loads((run / "run-state.json").read_text())["git_base"]
            (root / "服务.py").write_text("# TODO review committed change\n", encoding="utf-8")
            git("add", "服务.py")
            git("commit", "-qm", "changed")
            (root / "新 文件.py").write_text("# TODO review untracked change\n", encoding="utf-8")
            subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--set-phase", "verifying"], env=env, check=True, capture_output=True)
            self.assertEqual(json.loads((run / "run-state.json").read_text())["git_base"], baseline)
            result = subprocess.run([sys.executable, str(QUALITY), "--project", str(root), "--run", str(run), "--json", "--strict"], capture_output=True, text=True)
            findings = json.loads(result.stdout)["findings"]
            locations = {finding["location"] for finding in findings}
            self.assertIn("服务.py:1", locations)
            self.assertIn("新 文件.py:1", locations)
            self.assertNotEqual(result.returncode, 0)  # review evidence is missing

    def test_heuristic_logging_is_advisory_and_coverage_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True)
            (root / "service.py").write_text("def create():\n    return 1\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(QUALITY), "--project", str(root), "--strict"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("completed with warnings", result.stdout)
            self.assertIn("advisory", result.stdout)
            self.assertIn("No Git HEAD or run baseline", result.stdout)
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(QUALITY), "--project", tmp, "--json"], capture_output=True, text=True)
            self.assertTrue(any("not scanned" in finding["issue"] for finding in json.loads(result.stdout)["findings"]))

    def test_structural_evidence_requires_details_and_labelled_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            (run / "execution-log.md").write_text("failed\n", encoding="utf-8")
            (run / "evaluation.md").write_text("failed\n", encoding="utf-8")
            def check() -> subprocess.CompletedProcess:
                return subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--stage", "before-completion"], capture_output=True, text=True)
            self.assertNotEqual(check().returncode, 0)
            (run / "execution-log.md").write_text("- Commands:\n  - pytest\n- Result:\n  - passed\n", encoding="utf-8")
            (run / "evaluation.md").write_text("## Verification\nTests passed.\n", encoding="utf-8")
            result = check()
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("structure checked", result.stdout)
            (run / "execution-log.md").write_text("- RED command: pytest\n- RED result: failed as expected\n- GREEN command: pytest\n- GREEN result: passed\n", encoding="utf-8")
            self.assertEqual(check().returncode, 0)
            (run / "execution-log.md").write_text("- 命令：`python3 check_run.py`；通过。\n- 命令：检查 22 个文件，通过。\n", encoding="utf-8")
            (run / "evaluation.md").write_text("## 验收状态\n- 已完成验收。\n", encoding="utf-8")
            self.assertEqual(check().returncode, 0)
            (run / "execution-log.md").write_text("- 命令：`grep failed logfile`\n", encoding="utf-8")
            self.assertNotEqual(check().returncode, 0)
            (run / "plan.md").write_text("Fix the TODO: comment in foo.py\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--stage", "before-implementation"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)
            (run / "plan.md").write_text("- Needs decision: choose storage\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(CHECKER), str(run), "--tier", "xs", "--stage", "before-implementation"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_stop_rechecks_after_block_and_warns_without_infinite_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = root / "harness" / "runs" / "test"
            run.mkdir(parents=True)
            script = root / "harness" / "scripts" / "check_run.py"
            script.parent.mkdir(parents=True)
            script.write_bytes(CHECKER.read_bytes())
            (run / "execution-log.md").write_text("Command: pytest\nResult: passed\n", encoding="utf-8")
            state = {"schema_version": 1, "run": "test", "tier": "xs", "status": "verifying", "session_hash": hashlib.sha256(b"test").hexdigest()}
            (run / "run-state.json").write_text(json.dumps(state), encoding="utf-8")
            def stop(active: bool) -> dict:
                result = subprocess.run([sys.executable, str(HOOK), "Stop"], input=json.dumps({"cwd": str(root), "session_id": "test", "stop_hook_active": active}), capture_output=True, text=True, check=True, env={**os.environ, "CODEX_PLUGIN_ROOT": str(PLUGIN)})
                return json.loads(result.stdout)
            self.assertEqual(stop(False)["decision"], "block")
            retry = stop(True)
            self.assertTrue(retry["continue"])
            self.assertIn("still failing", retry["systemMessage"])
            self.assertEqual(json.loads((run / "run-state.json").read_text())["status"], "verifying")
            (run / "evaluation.md").write_text("Acceptance: passed\n", encoding="utf-8")
            self.assertTrue(stop(True)["continue"])
            self.assertEqual(json.loads((run / "run-state.json").read_text())["status"], "closed")


if __name__ == "__main__":
    unittest.main()

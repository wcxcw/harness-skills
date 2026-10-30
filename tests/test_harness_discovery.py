from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/harness-skills/skills/agent-harness"
INIT = SKILL / "scripts/init_harness.py"
DISCOVER = SKILL / "scripts/discover_project.py"


class ExistingHarnessSafetyTests(unittest.TestCase):
    def run_init(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INIT), "--project", str(project), "--language", "en", *args],
            capture_output=True,
            text=True,
        )

    def test_unknown_directory_is_preserved_until_explicitly_adopted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            existing = project / "harness" / "unrelated.txt"
            existing.parent.mkdir()
            existing.write_text("user data", encoding="utf-8")
            refused = self.run_init(project)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("Unrecognized nonempty harness directory", refused.stderr)
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual(existing.read_text(encoding="utf-8"), "user data")

            adopted = self.run_init(project, "--adopt-existing")
            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            self.assertTrue((project / "harness/scripts/check_run.py").is_file())
            self.assertEqual(existing.read_text(encoding="utf-8"), "user data")

    def test_existing_partial_harness_is_extended_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            gates = project / "harness/controls/gates.md"
            brief = project / "harness/context/project-brief.md"
            gates.parent.mkdir(parents=True)
            brief.parent.mkdir(parents=True)
            gates.write_text("custom gates", encoding="utf-8")
            brief.write_text("custom brief", encoding="utf-8")
            result = self.run_init(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(gates.read_text(encoding="utf-8"), "custom gates")
            self.assertEqual(brief.read_text(encoding="utf-8"), "custom brief")
            self.assertTrue((project / "harness/scripts/check_run.py").is_file())

    def test_symlinked_harness_is_never_followed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            project = Path(tmp)
            (project / "harness").symlink_to(Path(other), target_is_directory=True)
            result = self.run_init(project, "--adopt-existing")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertEqual(list(Path(other).iterdir()), [])

    def test_nested_symlink_cannot_write_outside_the_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            project = Path(tmp)
            harness = project / "harness"
            harness.mkdir()
            (harness / "context").symlink_to(Path(other), target_is_directory=True)
            result = self.run_init(project, "--adopt-existing")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside scaffold directory", result.stderr)
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual(list(Path(other).iterdir()), [])

    def test_partial_harness_can_be_identified_from_project_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "AGENTS.md").write_text("See harness/controls/gates.md", encoding="utf-8")
            gates = project / "harness/controls/gates.md"
            gates.parent.mkdir(parents=True)
            gates.write_text("project-owned gates", encoding="utf-8")
            result = self.run_init(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(gates.read_text(encoding="utf-8"), "project-owned gates")
            self.assertTrue((project / "harness/scripts/check_run.py").is_file())


class ProjectDiscoveryTests(unittest.TestCase):
    def test_mixed_project_is_read_only_and_reports_unverified_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for directory in ("frontend", "backend", ".github/workflows", "node_modules/pkg", ".vite/deps", "harness/runs/old"):
                (root / directory).mkdir(parents=True)
            (root / "package.json").write_text(json.dumps({"scripts": {"test": "touch SHOULD_NOT_EXIST", "deploy": "exit 9"}}))
            (root / "frontend/package.json").write_text(json.dumps({"scripts": {"build": "vite build"}}))
            (root / "backend/pom.xml").write_text("<project/>")
            (root / ".github/workflows/test.yml").write_text("name: test")
            (root / "node_modules/pkg/package.json").write_text('{"scripts":{"ignored":"false"}}')
            (root / ".vite/deps/package.json").write_text('{"scripts":{"ignored":"false"}}')
            (root / "harness/runs/old/package.json").write_text('{"scripts":{"ignored":"false"}}')
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            completed = subprocess.run([sys.executable, str(DISCOVER), "--project", str(root)], capture_output=True, text=True, check=True)
            result = json.loads(completed.stdout)
            self.assertEqual({x["source"] for x in result["manifests"]}, {"package.json", "frontend/package.json", "backend/pom.xml"})
            self.assertEqual({x["script"] for x in result["package_scripts"]}, {"test", "deploy", "build"})
            self.assertEqual([x["source"] for x in result["ci"]], [".github/workflows/test.yml"])
            self.assertTrue(all(x["status"] == "Discovered" and not x["verified"] and x["side_effects"] == "Not assessed" for x in result["package_scripts"]))
            self.assertFalse((root / "SHOULD_NOT_EXIST").exists())
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_bad_manifest_is_reported_without_executing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text("{")
            completed = subprocess.run([sys.executable, str(DISCOVER), "--project", str(root)], capture_output=True, text=True, check=True)
            result = json.loads(completed.stdout)
            self.assertEqual(result["errors"], [{"source": "package.json", "error": "JSONDecodeError"}])


if __name__ == "__main__":
    unittest.main()

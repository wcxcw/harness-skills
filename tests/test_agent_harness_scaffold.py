from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_MANIFEST = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_ROOT = ROOT / "plugins" / "harness-skills"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
INIT_SCRIPT = PLUGIN_ROOT / "skills" / "agent-harness" / "scripts" / "init_harness.py"
WORKFLOW_SKILLS = PLUGIN_ROOT / "skills" / "workflows"
VENDOR_SUPERPOWERS = ROOT / "vendor" / "superpowers"
QUALITY_CHECK = PLUGIN_ROOT / "scripts" / "quality_check.py"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
OPERATIONAL_WORKFLOW_SECTIONS = [
    "## Gate Mapping",
    "## Stop Conditions",
    "## Evidence Examples",
    "## Anti-Patterns",
]


class AgentHarnessScaffoldTest(unittest.TestCase):
    def test_plugin_exposes_only_harness_skills(self) -> None:
        manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["skills"], "./skills/")

        exposed_skills = (PLUGIN_ROOT / manifest["skills"]).resolve()
        self.assertTrue(exposed_skills.exists())
        self.assertNotIn("vendor", exposed_skills.parts)

        vendor_skill_files = list(VENDOR_SUPERPOWERS.glob("skills/**/SKILL.md"))
        self.assertTrue(vendor_skill_files)
        for vendor_skill in vendor_skill_files:
            self.assertFalse(vendor_skill.resolve().is_relative_to(exposed_skills), vendor_skill)

    def test_git_marketplace_manifest_points_to_plugin_wrapper(self) -> None:
        marketplace = json.loads(MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "harness-skills")
        [plugin] = marketplace["plugins"]
        self.assertEqual(plugin["name"], "harness-skills")
        self.assertEqual(plugin["source"], {"source": "local", "path": "./plugins/harness-skills"})
        self.assertEqual(plugin["policy"]["installation"], "AVAILABLE")
        plugin_path = (ROOT / plugin["source"]["path"]).resolve()
        self.assertEqual(plugin_path, PLUGIN_ROOT)
        self.assertEqual(plugin_path / ".codex-plugin" / "plugin.json", PLUGIN_MANIFEST)
        self.assertTrue(PLUGIN_MANIFEST.exists())

    def test_repository_uses_single_skills_source(self) -> None:
        root_skills = ROOT / "skills"
        plugin_skills = PLUGIN_ROOT / "skills"
        self.assertFalse(root_skills.exists())
        self.assertFalse((ROOT / ".codex-plugin").exists())
        self.assertFalse((ROOT / ".claude-plugin").exists())
        self.assertTrue(plugin_skills.is_dir())
        self.assertFalse(plugin_skills.is_symlink())

    def test_vendor_superpowers_curated_subset_is_present(self) -> None:
        expected = {
            "brainstorming",
            "writing-plans",
            "executing-plans",
            "test-driven-development",
            "systematic-debugging",
            "requesting-code-review",
            "receiving-code-review",
            "verification-before-completion",
            "writing-skills",
            "using-git-worktrees",
            "subagent-driven-development",
            "dispatching-parallel-agents",
        }
        actual = {path.parent.name for path in VENDOR_SUPERPOWERS.glob("skills/**/SKILL.md")}
        self.assertTrue(expected.issubset(actual), expected - actual)
        self.assertTrue((VENDOR_SUPERPOWERS / "NOTICE.md").exists())
        self.assertTrue((VENDOR_SUPERPOWERS / "LICENSE").exists())

    def test_installed_workflows_are_harness_adaptations(self) -> None:
        local_artifacts = {
            "workflow.md",
            "design.md",
            "spec.md",
            "plan.md",
            "execution-log.md",
            "review.md",
            "evaluation.md",
        }
        for skill_file in WORKFLOW_SKILLS.glob("**/SKILL.md"):
            text = skill_file.read_text(encoding="utf-8")
            self.assertNotIn("docs/superpowers", text, skill_file)
            self.assertNotIn("superpowers:", text, skill_file)
            self.assertTrue(
                "check_run.py" in text or "local gates" in text.lower(),
                f"{skill_file} does not mention local gate control",
            )
            self.assertTrue(
                any(artifact in text for artifact in local_artifacts),
                f"{skill_file} does not reference local Harness artifacts",
            )

    def test_workflow_skills_are_operational_procedures(self) -> None:
        workflow_skill_files = sorted(WORKFLOW_SKILLS.glob("*/SKILL.md"))
        self.assertTrue(workflow_skill_files)
        for skill_file in workflow_skill_files:
            text = skill_file.read_text(encoding="utf-8")
            for section in OPERATIONAL_WORKFLOW_SECTIONS:
                self.assertIn(section, text, f"{skill_file} missing {section}")
            for tier in ["`xs`", "`standard`", "`full`"]:
                self.assertIn(tier, text, f"{skill_file} missing tier {tier}")
            self.assertIn("check_run.py", text, f"{skill_file} missing local checker mapping")

    def test_core_profile_includes_gates_skills_and_checker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--profile",
                    "core",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            for rel in [
                "AGENTS.md",
                "harness/context/project-brief.md",
                "harness/context/coding-conventions.md",
                "harness/controls/gates.md",
                "harness/controls/risk-matrix.md",
                "harness/tools/commands.md",
                "harness/guardrails/boundaries.md",
                "harness/evals/task-scorecard.md",
                "harness/scripts/check_run.py",
                "harness/runs/.gitkeep",
            ]:
                self.assertTrue((project / rel).exists(), rel)
            for rel in [
                "harness/context/initialization-notes.md",
                "harness/controls/lifecycle.md",
                "harness/controls/skills.md",
                "harness/feedback/verification.md",
                "harness/context/repo-map.md",
                "harness/context/architecture.md",
                "harness/context/dependency-notes.md",
                "harness/guardrails/permissions.md",
                "harness/guardrails/rollback.md",
                "harness/evals/acceptance-checklist.md",
                "harness/evals/regression-checklist.md",
                "harness/specs/feature-template.md",
                "harness/specs/bugfix-template.md",
            ]:
                self.assertFalse((project / rel).exists(), rel)

    def test_quality_workflows_are_exposed_and_scaffolded(self) -> None:
        expected_skills = {
            "code-quality-review",
            "frontend-quality-review",
            "backend-quality-review",
            "receiving-code-review",
            "context-budget",
            "code-reviewer",
        }
        actual_skills = {path.parent.name for path in WORKFLOW_SKILLS.glob("*/SKILL.md")}
        self.assertTrue(expected_skills.issubset(actual_skills), expected_skills - actual_skills)

        workflows = (WORKFLOW_SKILLS / "SKILL.md").read_text(encoding="utf-8")
        related = (
            PLUGIN_ROOT
            / "skills"
            / "agent-harness"
            / "references"
            / "related-skills.md"
        ).read_text(encoding="utf-8")
        agent_harness = (PLUGIN_ROOT / "skills" / "agent-harness" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("code-quality-review/SKILL.md", workflows)
        self.assertIn("frontend-quality-review/SKILL.md", workflows)
        self.assertIn("backend-quality-review/SKILL.md", workflows)
        self.assertIn("receiving-code-review/SKILL.md", workflows)
        self.assertIn("context-budget/SKILL.md", workflows)
        self.assertIn("code-reviewer/SKILL.md", workflows)
        self.assertIn("Code quality is a completion gate", agent_harness)
        self.assertIn("frontend-quality-review", related)
        self.assertIn("code-reviewer", related)
        requesting_review = (WORKFLOW_SKILLS / "requesting-code-review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("This skill is the review coordinator", requesting_review)
        self.assertIn("Do not run every review skill mechanically", requesting_review)

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--profile",
                    "core",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            agents = (project / "AGENTS.md").read_text(encoding="utf-8")
            conventions = (project / "harness" / "context" / "coding-conventions.md").read_text(encoding="utf-8")
            scorecard = (project / "harness" / "evals" / "task-scorecard.md").read_text(encoding="utf-8")
            gates = (project / "harness" / "controls" / "gates.md").read_text(encoding="utf-8")
            risk_matrix = (project / "harness" / "controls" / "risk-matrix.md").read_text(encoding="utf-8")

            self.assertIn("run code-quality review before final verification", agents)
            self.assertIn("App.vue", conventions)
            self.assertIn("logging, error handling, and testability gaps", conventions)
            self.assertIn("Code-quality review was run", scorecard)
            self.assertIn("Application code changes received code-quality review", gates)
            self.assertIn("Data loss", risk_matrix)

    def test_plugin_hooks_and_quality_script_are_present(self) -> None:
        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        self.assertIn("SessionStart", hooks["hooks"])
        self.assertIn("Stop", hooks["hooks"])
        self.assertIn("harness_hook.py", json.dumps(hooks))
        self.assertTrue((PLUGIN_ROOT / "scripts" / "harness_hook.py").exists())
        self.assertTrue(QUALITY_CHECK.exists())

    def test_quality_check_blocks_missing_code_quality_review_for_code_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            src = project / "src"
            src.mkdir()
            app = src / "App.vue"
            app.write_text("<template><main>ok</main></template>\n", encoding="utf-8")
            subprocess.run(["git", "init"], cwd=project, check=True, capture_output=True, text=True)
            subprocess.run(["git", "add", "."], cwd=project, check=True, capture_output=True, text=True)
            subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "-m", "init"],
                cwd=project,
                check=True,
                capture_output=True,
                text=True,
            )

            app.write_text(
                "<script setup>\nconst state = ref(null)\nfetch('/api/items')\n</script>\n"
                + "\n".join(f"// line {index}" for index in range(220)),
                encoding="utf-8",
            )
            run_dir = project / "harness" / "runs" / "2026-06-05-test"
            run_dir.mkdir(parents=True)

            result = subprocess.run(
                [sys.executable, str(QUALITY_CHECK), "--project", str(project), "--run", str(run_dir), "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no code-quality review or skip reason", result.stdout)

    def test_generated_agents_uses_selective_context_loading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            en_project = Path(tmp) / "en"
            zh_project = Path(tmp) / "zh"
            for project, language in [(en_project, "en"), (zh_project, "zh-CN")]:
                subprocess.run(
                    [
                        sys.executable,
                        str(INIT_SCRIPT),
                        "--project",
                        str(project),
                        "--profile",
                        "core",
                        "--language",
                        language,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            en_agents = (en_project / "AGENTS.md").read_text(encoding="utf-8")
            zh_agents = (zh_project / "AGENTS.md").read_text(encoding="utf-8")
            agent_harness = (PLUGIN_ROOT / "skills" / "agent-harness" / "SKILL.md").read_text(encoding="utf-8")

            self.assertIn("Do not bulk-read `harness/context/*` or `harness/runs/*`", en_agents)
            self.assertIn("1. `harness/context/project-brief.md`", en_agents)
            self.assertIn("when maintaining it, keep it to a short project summary", en_agents)
            self.assertIn("Prefer targeted search or section reads", en_agents)
            self.assertIn("不要批量读取 `harness/context/*` 或 `harness/runs/*`", zh_agents)
            self.assertIn("1. `harness/context/project-brief.md`", zh_agents)
            self.assertIn("维护或更新该文件时，只保留短项目摘要", zh_agents)
            self.assertIn("按章节读取", zh_agents)
            self.assertIn("Load context on demand", agent_harness)

    def test_run_boundary_guidance_reuses_active_run_for_followups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            en_project = Path(tmp) / "en"
            zh_project = Path(tmp) / "zh"
            for project, language in [(en_project, "en"), (zh_project, "zh-CN")]:
                subprocess.run(
                    [
                        sys.executable,
                        str(INIT_SCRIPT),
                        "--project",
                        str(project),
                        "--profile",
                        "core",
                        "--language",
                        language,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            en_agents = (en_project / "AGENTS.md").read_text(encoding="utf-8")
            en_gates = (en_project / "harness" / "controls" / "gates.md").read_text(encoding="utf-8")
            en_gates_normalized = " ".join(en_gates.split())
            zh_agents = (zh_project / "AGENTS.md").read_text(encoding="utf-8")
            zh_gates = (zh_project / "harness" / "controls" / "gates.md").read_text(encoding="utf-8")
            lifecycle = (
                PLUGIN_ROOT
                / "skills"
                / "agent-harness"
                / "assets"
                / "templates"
                / "harness"
                / "controls"
                / "lifecycle.md"
            ).read_text(encoding="utf-8")
            executing = (WORKFLOW_SKILLS / "executing-plans" / "SKILL.md").read_text(encoding="utf-8")

            self.assertIn("Run eligibility, tiers, and boundaries are defined in `harness/controls/gates.md`", en_agents)
            self.assertIn("keep one active run per user objective", en_agents)
            self.assertIn("Do not create a new run for a small fix to the same objective", en_gates_normalized)
            self.assertIn("A run represents a user objective", lifecycle)
            self.assertIn("continue the active run", executing)

            self.assertIn("Run 是否需要、分级和边界以 `harness/controls/gates.md` 为准", zh_agents)
            self.assertIn("一个用户目标对应一个 active run", zh_agents)
            self.assertIn("不要因为同一目标下的小修复新建 run", zh_gates)

    def test_micro_change_guidance_allows_no_run_direct_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            en_project = Path(tmp) / "en"
            zh_project = Path(tmp) / "zh"
            for project, language in [(en_project, "en"), (zh_project, "zh-CN")]:
                subprocess.run(
                    [
                        sys.executable,
                        str(INIT_SCRIPT),
                        "--project",
                        str(project),
                        "--profile",
                        "core",
                        "--language",
                        language,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            en_agents = (en_project / "AGENTS.md").read_text(encoding="utf-8")
            en_gates = (en_project / "harness" / "controls" / "gates.md").read_text(encoding="utf-8")
            zh_agents = (zh_project / "AGENTS.md").read_text(encoding="utf-8")
            zh_gates = (zh_project / "harness" / "controls" / "gates.md").read_text(encoding="utf-8")
            agent_harness = (PLUGIN_ROOT / "skills" / "agent-harness" / "SKILL.md").read_text(encoding="utf-8")
            readme = (ROOT / "README.md").read_text(encoding="utf-8")

            self.assertIn("If gates classify the request as a no-run micro change", en_agents)
            self.assertIn("behavior-preserving, decision-free", en_gates)
            self.assertIn("Not micro: broad visual", en_gates)
            self.assertIn("Run tiers apply only when a run is warranted", en_gates)
            self.assertIn("all micro-change criteria are met", readme)
            self.assertIn("typography hierarchy changes", readme)
            self.assertIn("Skip run creation for explicit, low-risk micro changes", agent_harness)
            self.assertIn("no-run micro change only when all of these are true", agent_harness)

            self.assertIn("gates 判定为 no-run 微小改动", zh_agents)
            self.assertIn("必须同时满足", zh_gates)
            self.assertIn("非微小改动", zh_gates)
            self.assertIn("只有需要 run 时才选择 run tier", zh_gates)
            self.assertIn("宽泛视觉", zh_gates)

    def test_scaffold_only_accepts_core_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            for profile in ["brownfield", "full"]:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(INIT_SCRIPT),
                        "--project",
                        str(project),
                        "--profile",
                        profile,
                        "--language",
                        "en",
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid choice", result.stderr)

    def test_generated_checker_enforces_run_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-06-03-test"
            subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--profile",
                    "core",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            run_dir.mkdir(parents=True)

            checker = project / "harness" / "scripts" / "check_run.py"
            failed = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "before-implementation"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("Missing workflow.md", failed.stdout)
            self.assertIn("Missing spec.md", failed.stdout)

            (run_dir / "workflow.md").write_text(
                """# Workflow

## Skills Used
- brainstorming
- writing-specs
- writing-plans

## Gates
- before-implementation: pending
- before-completion: pending
""",
                encoding="utf-8",
            )
            (run_dir / "spec.md").write_text(
                """# Spec

## Objective
Ship a test change.

## In Scope
- Test scope.

## Out of Scope
- Unrelated work.

## Acceptance Criteria
- [ ] Criteria is met.

## Verification
- [ ] Run tests.

## Open Questions
None.
""",
                encoding="utf-8",
            )
            (run_dir / "plan.md").write_text(
                """# Plan

## Tasks
- Task 1: implement the change.

## Verification
- Run tests.
""",
                encoding="utf-8",
            )
            (run_dir / "execution-log.md").write_text(
                "Command: python -m unittest\nResult: passed\n",
                encoding="utf-8",
            )
            (run_dir / "review.md").write_text(
                """# Review

## Review
No findings.
""",
                encoding="utf-8",
            )
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nRisk: no residual risk.\n",
                encoding="utf-8",
            )

            passed = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "all"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_xs_tier_requires_only_completion_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-06-03-xs"
            subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--profile",
                    "core",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            run_dir.mkdir(parents=True)
            (run_dir / "execution-log.md").write_text(
                "Manual check: updated one doc line\nResult: passed\n",
                encoding="utf-8",
            )
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nRisk: none\n",
                encoding="utf-8",
            )

            checker = project / "harness" / "scripts" / "check_run.py"
            result = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "all", "--tier", "xs"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_closed_loop_run_lifecycle_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-06-03-closed-loop"
            subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--profile",
                    "core",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            run_dir.mkdir(parents=True)
            for rel in [
                "harness/controls/gates.md",
                "harness/scripts/check_run.py",
            ]:
                self.assertTrue((project / rel).exists(), rel)

            (run_dir / "input.md").write_text("Add closed-loop verification.\n", encoding="utf-8")
            (run_dir / "workflow.md").write_text(
                """# Workflow

## Skills Used
- brainstorming
- writing-specs
- writing-plans
- executing-plans
- requesting-code-review
- verification-before-completion
- finishing-run

## Gates
- before-implementation: passed
- before-completion: passed
""",
                encoding="utf-8",
            )
            (run_dir / "design.md").write_text(
                """# Design

## Problem
The harness needs a closed-loop run contract.
""",
                encoding="utf-8",
            )
            (run_dir / "spec.md").write_text(
                """# Spec

## Objective
Prove a closed-loop run can pass local gates.

## In Scope
- Lifecycle artifacts.

## Out of Scope
- Application code.

## Acceptance Criteria
- [ ] All required run artifacts exist.

## Verification
- [ ] Run the local checker.

## Open Questions
None.
""",
                encoding="utf-8",
            )
            (run_dir / "plan.md").write_text(
                """# Plan

## Tasks
- Create lifecycle artifacts.

## Verification
- Run check_run.py.
""",
                encoding="utf-8",
            )
            (run_dir / "execution-log.md").write_text(
                "Command: python3 harness/scripts/check_run.py harness/runs/2026-06-03-closed-loop --stage all\nResult: passed\n",
                encoding="utf-8",
            )
            (run_dir / "review.md").write_text(
                """# Review

## Review
No findings.
""",
                encoding="utf-8",
            )
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nVerification: passed\nRisk: none\n",
                encoding="utf-8",
            )

            checker = project / "harness" / "scripts" / "check_run.py"
            result = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "all", "--tier", "full"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

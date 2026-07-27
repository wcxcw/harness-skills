from __future__ import annotations

import json
import os
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
GRILL_SKILL = WORKFLOW_SKILLS / "grilling" / "SKILL.md"
GRILL_METADATA = WORKFLOW_SKILLS / "grilling" / "agents" / "openai.yaml"
VENDOR_SUPERPOWERS = ROOT / "vendor" / "superpowers"
QUALITY_CHECK = PLUGIN_ROOT / "scripts" / "quality_check.py"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
HARNESS_HOOK = PLUGIN_ROOT / "scripts" / "harness_hook.py"
PRE_RUN_WORKFLOWS = {"grilling"}
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
            "spec.md",
            "plan.md",
            "execution-log.md",
            "review.md",
            "evaluation.md",
        }
        for skill_file in WORKFLOW_SKILLS.glob("**/SKILL.md"):
            if skill_file.parent.name in PRE_RUN_WORKFLOWS:
                continue
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
            if skill_file.parent.name in PRE_RUN_WORKFLOWS:
                continue
            text = skill_file.read_text(encoding="utf-8")
            for section in OPERATIONAL_WORKFLOW_SECTIONS:
                self.assertIn(section, text, f"{skill_file} missing {section}")
            for tier in ["`xs`", "`standard`", "`full`"]:
                self.assertIn(tier, text, f"{skill_file} missing tier {tier}")
            self.assertIn("check_run.py", text, f"{skill_file} missing local checker mapping")

    def test_grilling_is_manual_pre_run_alignment_without_artifacts(self) -> None:
        self.assertTrue(GRILL_SKILL.exists())
        self.assertTrue(GRILL_METADATA.exists())

        grill = GRILL_SKILL.read_text(encoding="utf-8")
        metadata = GRILL_METADATA.read_text(encoding="utf-8")
        workflows = (WORKFLOW_SKILLS / "SKILL.md").read_text(encoding="utf-8")
        agent_harness = (PLUGIN_ROOT / "skills" / "agent-harness" / "SKILL.md").read_text(encoding="utf-8")
        writing_specs = (WORKFLOW_SKILLS / "writing-specs" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("explicitly invokes", grill)
        self.assertIn("one question at a time", grill)
        self.assertIn("recommended answer", grill)
        self.assertIn("explore the repository", grill.lower())
        self.assertIn("Do not create or update Harness artifacts", grill)
        self.assertIn("shared understanding", grill)
        for artifact in [
            "workflow.md",
            "design.md",
            "spec.md",
            "plan.md",
            "execution-log.md",
            "review.md",
            "evaluation.md",
        ]:
            self.assertNotIn(artifact, grill)

        self.assertIn("allow_implicit_invocation: false", metadata)
        self.assertIn("$grilling", metadata)
        self.assertLess(workflows.index("`grilling/SKILL.md`"), workflows.index("`writing-specs/SKILL.md`"))
        self.assertIn("before creating a run", agent_harness)
        self.assertIn("`grilling`", agent_harness)
        self.assertFalse((WORKFLOW_SKILLS / "brainstorming").exists())
        self.assertNotIn("brainstorming/SKILL.md", workflows)
        self.assertNotIn("`brainstorming`", agent_harness)
        self.assertIn("confirmed shared understanding", writing_specs)

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

    def test_code_reviewer_follows_active_run_language(self) -> None:
        code_reviewer = (WORKFLOW_SKILLS / "code-reviewer" / "SKILL.md").read_text(encoding="utf-8")
        reviewer_prompt = (WORKFLOW_SKILLS / "code-reviewer" / "prompt.md").read_text(encoding="utf-8")
        review_coordinator = (WORKFLOW_SKILLS / "requesting-code-review" / "SKILL.md").read_text(encoding="utf-8")

        for text in [code_reviewer, reviewer_prompt]:
            self.assertIn("active run language", text)
            self.assertIn("If the objective", text)
            self.assertIn("Chinese", text)
            self.assertIn("## 发现", text)
            self.assertIn("## 剩余风险", text)
            self.assertIn("严重程度", text)
            self.assertIn("位置", text)
            self.assertIn("必需操作", text)
            self.assertIn("Do not keep English", text)

        self.assertIn("owns the complete `review.md`", code_reviewer)
        self.assertIn("structured review contribution only", reviewer_prompt)
        self.assertIn("## Review Scope", review_coordinator)
        self.assertIn("## Review 范围", review_coordinator)
        self.assertIn("## Findings", review_coordinator)
        self.assertIn("## 发现", review_coordinator)
        self.assertIn("## Resolution", review_coordinator)
        self.assertIn("## 处理结果", review_coordinator)
        self.assertIn("## Residual Risk", review_coordinator)
        self.assertIn("## 剩余风险", review_coordinator)
        self.assertIn("do not add a duplicate `## Review` sentinel", review_coordinator)

        for skill_name in ["code-quality-review", "frontend-quality-review", "backend-quality-review"]:
            quality_review = (WORKFLOW_SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("`requesting-code-review` merges it", quality_review)
            self.assertIn("### ", quality_review)

    def test_plugin_hooks_and_quality_script_are_present(self) -> None:
        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        self.assertEqual(set(hooks), {"hooks"})
        self.assertIn("SessionStart", hooks["hooks"])
        self.assertIn("Stop", hooks["hooks"])
        self.assertIn("harness_hook.py", json.dumps(hooks))
        self.assertTrue((PLUGIN_ROOT / "scripts" / "harness_hook.py").exists())
        self.assertTrue(QUALITY_CHECK.exists())
        hook_script = (PLUGIN_ROOT / "scripts" / "harness_hook.py").read_text(encoding="utf-8")
        self.assertIn("reuse it within the same", hook_script)
        self.assertIn("explicitly invoke $grilling", hook_script)
        self.assertIn("verifying_runs", hook_script)
        self.assertNotIn("latest_run", hook_script)
        self.assertNotIn("infer_tier", hook_script)

    def test_workflows_define_session_scoped_run_lifecycle(self) -> None:
        agent_harness = (PLUGIN_ROOT / "skills" / "agent-harness" / "SKILL.md").read_text(encoding="utf-8")
        executing = (WORKFLOW_SKILLS / "executing-plans" / "SKILL.md").read_text(encoding="utf-8")
        requesting_review = (WORKFLOW_SKILLS / "requesting-code-review" / "SKILL.md").read_text(encoding="utf-8")
        receiving_review = (WORKFLOW_SKILLS / "receiving-code-review" / "SKILL.md").read_text(encoding="utf-8")
        finishing = (WORKFLOW_SKILLS / "finishing-run" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("run-state.json", agent_harness)
        self.assertIn("--set-phase active", agent_harness)
        self.assertIn("--set-phase verifying", agent_harness)
        self.assertIn("--set-phase closed", agent_harness)
        self.assertIn("--set-phase active", executing)
        self.assertIn("--set-phase reviewing", requesting_review)
        self.assertIn("phase to `reviewing`", receiving_review)
        self.assertIn("--set-phase verifying", finishing)
        self.assertIn("session-scoped Stop hook", finishing)

    def test_stop_hook_only_gates_current_session_when_verifying(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-07-27-session-gate"
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
            (run_dir / "execution-log.md").write_text("Command: tests\nResult: passed\n", encoding="utf-8")
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nVerification: passed\nRisk: none\n",
                encoding="utf-8",
            )
            (run_dir / "review.md").write_text("# Review\n\n## Review Scope\nScope only.\n", encoding="utf-8")
            checker = project / "harness" / "scripts" / "check_run.py"

            def run_hook(session_id: str) -> dict:
                completed = subprocess.run(
                    [sys.executable, str(HARNESS_HOOK), "Stop"],
                    input=json.dumps({"cwd": str(project), "session_id": session_id}),
                    capture_output=True,
                    text=True,
                    check=True,
                    env={**os.environ, "CODEX_PLUGIN_ROOT": str(PLUGIN_ROOT)},
                )
                return json.loads(completed.stdout)

            def set_phase(phase: str, session_id: str = "session-a", tier: str = "full") -> None:
                subprocess.run(
                    [
                        sys.executable,
                        str(checker),
                        str(run_dir),
                        "--tier",
                        tier,
                        "--set-phase",
                        phase,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "CODEX_THREAD_ID": session_id},
                )

            self.assertEqual(run_hook("session-a"), {"continue": True})

            no_session_env = {
                key: value
                for key, value in os.environ.items()
                if key not in {"CODEX_THREAD_ID", "CLAUDE_SESSION_ID"}
            }
            no_session = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    str(run_dir),
                    "--tier",
                    "full",
                    "--set-phase",
                    "active",
                ],
                capture_output=True,
                text=True,
                env=no_session_env,
            )
            self.assertNotEqual(no_session.returncode, 0)
            self.assertIn("No session ID is available", no_session.stderr)

            set_phase("active")
            self.assertEqual(run_hook("session-a"), {"continue": True})

            set_phase("reviewing")
            self.assertEqual(run_hook("session-a"), {"continue": True})

            set_phase("verifying")
            self.assertEqual(run_hook("session-b"), {"continue": True})
            blocked = run_hook("session-a")
            self.assertEqual(blocked["decision"], "block")
            self.assertIn("missing required section: findings", blocked["reason"])

            (run_dir / "review.md").write_text(
                """# Review

## Review Scope
Current run behavior.

## Findings
None.

## Resolution
No action required.

## Residual Risk
None.
""",
                encoding="utf-8",
            )
            passed = run_hook("session-a")
            self.assertEqual(passed, {"continue": True})
            state = json.loads((run_dir / "run-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "closed")
            self.assertNotIn("session_hash", state)
            self.assertEqual(run_hook("session-a"), {"continue": True})

            (run_dir / "review.md").write_text("# Review\n\n## Review Scope\nScope only.\n", encoding="utf-8")
            set_phase("verifying", tier="standard")
            self.assertEqual(run_hook("session-a"), {"continue": True})
            state = json.loads((run_dir / "run-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["tier"], "standard")
            self.assertEqual(state["status"], "closed")

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

    def test_quality_check_detects_and_resolves_chinese_review_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-07-26-chinese-review"
            run_dir.mkdir(parents=True)
            review = run_dir / "review.md"
            review.write_text(
                """# Review

## 发现
- 严重程度：Important
- 位置：`src/export.py:10`
- 问题：导出失败未被报告。
- 必需操作：补充错误处理。
- 处理结果：pending
""",
                encoding="utf-8",
            )

            unresolved = subprocess.run(
                [sys.executable, str(QUALITY_CHECK), "--project", str(project), "--run", str(run_dir), "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(unresolved.returncode, 0)
            self.assertIn("unresolved Critical or Important finding", unresolved.stdout)

            review.write_text(
                review.read_text(encoding="utf-8").replace("处理结果：pending", "处理结果：已修复"),
                encoding="utf-8",
            )
            resolved = subprocess.run(
                [sys.executable, str(QUALITY_CHECK), "--project", str(project), "--run", str(run_dir), "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)

    def test_quality_check_treats_only_comment_markers_as_temporary_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            script = project / "check.py"
            script.write_text("MARKERS = []\n", encoding="utf-8")
            subprocess.run(["git", "init"], cwd=project, check=True, capture_output=True, text=True)
            subprocess.run(["git", "add", "."], cwd=project, check=True, capture_output=True, text=True)
            subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "-m", "init"],
                cwd=project,
                check=True,
                capture_output=True,
                text=True,
            )

            script.write_text('MARKERS = ["TODO:", "FIXME"]\n', encoding="utf-8")
            schema_literals = subprocess.run(
                [sys.executable, str(QUALITY_CHECK), "--project", str(project)],
                capture_output=True,
                text=True,
            )
            self.assertNotIn("Temporary marker remains", schema_literals.stdout)

            temporary_comment = "# " + "TODO remove temporary fallback\n"
            script.write_text('MARKERS = ["TODO:"]\n' + temporary_comment, encoding="utf-8")
            comment_marker = subprocess.run(
                [sys.executable, str(QUALITY_CHECK), "--project", str(project)],
                capture_output=True,
                text=True,
            )
            self.assertIn("Temporary marker remains", comment_marker.stdout)

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
            self.assertIn("reuse an already-loaded `project-brief.md`", en_agents)
            self.assertIn("Prefer targeted search or section reads", en_agents)
            self.assertIn("explicitly invoke `$grilling`", en_agents)
            self.assertIn("before creating a run", en_agents)
            self.assertIn("不要批量读取 `harness/context/*` 或 `harness/runs/*`", zh_agents)
            self.assertIn("1. `harness/context/project-brief.md`", zh_agents)
            self.assertIn("维护或更新该文件时，只保留短项目摘要", zh_agents)
            self.assertIn("应复用已加载内容", zh_agents)
            self.assertIn("按章节读取", zh_agents)
            self.assertIn("显式调用 `$grilling`", zh_agents)
            self.assertIn("创建 run 前", zh_agents)
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
            self.assertTrue("all micro-change criteria are met" in readme or "微小改动条件" in readme)
            self.assertTrue("typography hierarchy changes" in readme or "整体字体层级调整" in readme)
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

    def test_scaffold_can_update_only_the_local_checker(self) -> None:
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
            agents = project / "AGENTS.md"
            checker = project / "harness" / "scripts" / "check_run.py"
            agents.write_text("project-specific instructions\n", encoding="utf-8")
            checker.write_text("# stale checker\n", encoding="utf-8")

            updated = subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--project",
                    str(project),
                    "--update-checker",
                    "--language",
                    "en",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(agents.read_text(encoding="utf-8"), "project-specific instructions\n")
            self.assertNotIn("stale checker", checker.read_text(encoding="utf-8"))
            self.assertIn("--set-phase", checker.read_text(encoding="utf-8"))
            self.assertIn("Updated Agent Harness checker", updated.stdout)

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

## Alignment
- Source: user-provided brief
- Confirmed by user: no

## Objective
Ship a test change.
- Confirmed by user: yes

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

## Review Scope
Test scope.

## Findings
No findings.

## Resolution
No action required.

## Residual Risk
None.
""",
                encoding="utf-8",
            )
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nRisk: no residual risk.\n",
                encoding="utf-8",
            )

            unconfirmed = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "before-implementation"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(unconfirmed.returncode, 0)
            self.assertIn("user-confirmed alignment", unconfirmed.stdout)
            spec_path = run_dir / "spec.md"
            spec_path.write_text(
                spec_path.read_text(encoding="utf-8").replace(
                    "- Confirmed by user: no",
                    "- Confirmed by user: yes",
                ),
                encoding="utf-8",
            )

            passed = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "all"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_generated_checker_accepts_chinese_alignment_confirmation(self) -> None:
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
                    "zh-CN",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            run_dir = project / "harness" / "runs" / "2026-06-03-zh-alignment"
            run_dir.mkdir(parents=True)
            (run_dir / "workflow.md").write_text(
                "# 工作流\n\n## 使用的 Skills\n- writing-specs\n- writing-plans\n\n## 门槛\n- 实现前：待检查\n",
                encoding="utf-8",
            )
            (run_dir / "spec.md").write_text(
                "# 规格\n\n## 对齐确认\n- 来源：grilling\n- 用户已确认：是\n\n## 目标\n完成测试。\n\n## 范围内\n- 测试。\n\n## 非目标\n- 其他修改。\n\n## 验收标准\n- 检查通过。\n\n## 验证\n- 运行检查。\n\n## 待确认问题\n无。\n",
                encoding="utf-8",
            )
            (run_dir / "plan.md").write_text(
                "# 计划\n\n## 任务\n- 执行修改。\n\n## 验证\n- 运行检查。\n",
                encoding="utf-8",
            )

            checker = project / "harness" / "scripts" / "check_run.py"
            result = subprocess.run(
                [sys.executable, str(checker), str(run_dir), "--stage", "before-implementation"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generated_checker_enforces_bilingual_review_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            run_dir = project / "harness" / "runs" / "2026-07-26-review-schema"
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
                "Command: python -m unittest\nResult: passed\n",
                encoding="utf-8",
            )
            (run_dir / "evaluation.md").write_text(
                "Acceptance: passed\nVerification: passed\nRisk: none\n",
                encoding="utf-8",
            )
            checker = project / "harness" / "scripts" / "check_run.py"
            review_documents = [
                """# Review

## Review Scope
Changed files and acceptance criteria.

## Findings
No findings.

## Resolution
No action required.

## Residual Risk
None.
""",
                """# Review

## Review 范围
变更文件与验收标准。

## 发现
无发现。

## 处理结果
无需处理。

## 剩余风险
无。
""",
            ]

            for review_text in review_documents:
                with self.subTest(review_text=review_text):
                    (run_dir / "review.md").write_text(review_text, encoding="utf-8")
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(checker),
                            str(run_dir),
                            "--stage",
                            "before-completion",
                            "--tier",
                            "full",
                        ],
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            required_blocks = {
                "review_scope": "## Review Scope\nChanged files and acceptance criteria.\n\n",
                "findings": "## Findings\nNo findings.\n\n",
                "resolution": "## Resolution\nNo action required.\n\n",
                "residual_risk": "## Residual Risk\nNone.\n",
            }
            for section, block in required_blocks.items():
                with self.subTest(missing_section=section):
                    (run_dir / "review.md").write_text(
                        review_documents[0].replace(block, ""),
                        encoding="utf-8",
                    )
                    missing_section = subprocess.run(
                        [
                            sys.executable,
                            str(checker),
                            str(run_dir),
                            "--stage",
                            "before-completion",
                            "--tier",
                            "full",
                        ],
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(missing_section.returncode, 0)
                    self.assertIn(
                        f"review.md is missing required section: {section}",
                        missing_section.stdout,
                    )

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
            (run_dir / "spec.md").write_text(
                """# Spec

## Alignment
- Source: grilling
- Confirmed by user: yes

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

## Review Scope
Closed-loop lifecycle artifacts.

## Findings
No findings.

## Resolution
No action required.

## Residual Risk
None.
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

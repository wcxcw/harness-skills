#!/usr/bin/env python3
"""Initialize a project-level Agent Harness from bundled templates."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


CORE_HARNESS_FILES = [
    "context/project-brief.md",
    "context/initialization-notes.md",
    "tools/commands.md",
    "feedback/verification.md",
    "guardrails/boundaries.md",
    "evals/task-scorecard.md",
    "runs/.gitkeep",
]

BROWNFIELD_EXTRA_FILES = [
    "context/repo-map.md",
    "context/architecture.md",
    "context/coding-conventions.md",
    "context/dependency-notes.md",
]


def copy_tree(src: Path, dst: Path, force: bool) -> list[Path]:
    written: list[Path] = []
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        written.append(target)
    return written


def copy_files(src: Path, dst: Path, files: list[str], force: bool) -> list[Path]:
    written: list[Path] = []
    for rel_name in files:
        source = src / rel_name
        if not source.exists():
            raise SystemExit(f"Template file not found: {source}")
        target = dst / rel_name
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Agent Harness files in a project.")
    parser.add_argument("--project", default=".", help="Project root to scaffold into.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument(
        "--profile",
        choices=["core", "brownfield", "full"],
        default="core",
        help="Template set to scaffold. core is minimal; brownfield adds repository context files; full copies every bundled template.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    templates = skill_dir / "assets" / "templates"
    project = Path(args.project).resolve()

    if not templates.exists():
        raise SystemExit(f"Template directory not found: {templates}")

    written = copy_tree(templates / "root", project, args.force)
    harness_templates = templates / "harness"
    if args.profile == "full":
        written += copy_tree(harness_templates, project / "harness", args.force)
    else:
        harness_files = list(CORE_HARNESS_FILES)
        if args.profile == "brownfield":
            harness_files += BROWNFIELD_EXTRA_FILES
        written += copy_files(harness_templates, project / "harness", harness_files, args.force)
    (project / "harness" / "runs").mkdir(parents=True, exist_ok=True)

    print(f"Initialized Agent Harness in {project} using profile: {args.profile}")
    if written:
        print("Files written:")
        for path in written:
            print(f"- {path.relative_to(project)}")
    else:
        print("No files written; existing files were preserved. Use --force to overwrite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

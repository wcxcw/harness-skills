#!/usr/bin/env python3
"""Initialize a project-level Agent Harness from bundled templates."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


CORE_HARNESS_FILES = [
    "context/project-brief.md",
    "controls/gates.md",
    "tools/commands.md",
    "guardrails/boundaries.md",
    "scripts/check_run.py",
    "runs/.gitkeep",
]

def localized_source(path: Path, language: str) -> Path:
    if language == "en":
        return path
    candidate = path.with_name(f"{path.stem}.{language}{path.suffix}")
    if candidate.exists():
        return candidate
    return path


def should_skip_template(path: Path) -> bool:
    return any(part in {"zh-CN"} for part in path.parts) or path.stem.endswith(".zh-CN")


def resolve_language(requested: str) -> str:
    if requested != "auto":
        return requested
    locale = " ".join(
        os.environ.get(name, "") for name in ("LC_ALL", "LC_MESSAGES", "LANG")
    ).lower()
    if "zh" in locale:
        return "zh-CN"
    return "en"


def copy_tree(src: Path, dst: Path, force: bool, language: str) -> list[Path]:
    written: list[Path] = []
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if should_skip_template(path):
            continue
        source = localized_source(path, language)
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        written.append(target)
    return written


def copy_files(src: Path, dst: Path, files: list[str], force: bool, language: str) -> list[Path]:
    written: list[Path] = []
    for rel_name in files:
        source = src / rel_name
        if not source.exists():
            raise SystemExit(f"Template file not found: {source}")
        source = localized_source(source, language)
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
        choices=["core"],
        default="core",
        help="Template set to scaffold. Only core is supported; it creates the minimal harness.",
    )
    parser.add_argument(
        "--language",
        choices=["auto", "en", "zh-CN"],
        default="auto",
        help="Template language. auto follows the process locale; use zh-CN for Chinese harness files.",
    )
    args = parser.parse_args()
    language = resolve_language(args.language)

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    templates = skill_dir / "assets" / "templates"
    project = Path(args.project).resolve()

    if not templates.exists():
        raise SystemExit(f"Template directory not found: {templates}")

    written = copy_tree(templates / "root", project, args.force, language)
    harness_templates = templates / "harness"
    written += copy_files(harness_templates, project / "harness", CORE_HARNESS_FILES, args.force, language)
    (project / "harness" / "runs").mkdir(parents=True, exist_ok=True)

    print(f"Initialized Agent Harness in {project} using profile: {args.profile}, language: {language}")
    if written:
        print("Files written:")
        for path in written:
            print(f"- {path.relative_to(project)}")
    else:
        print("No files written; existing files were preserved. Use --force to overwrite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

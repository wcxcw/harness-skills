#!/usr/bin/env python3
"""Initialize a project-level Agent Harness from bundled templates."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Agent Harness files in a project.")
    parser.add_argument("--project", default=".", help="Project root to scaffold into.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    templates = skill_dir / "assets" / "templates"
    project = Path(args.project).resolve()

    if not templates.exists():
        raise SystemExit(f"Template directory not found: {templates}")

    written = copy_tree(templates / "root", project, args.force)
    written += copy_tree(templates / "harness", project / "harness", args.force)
    (project / "harness" / "runs").mkdir(parents=True, exist_ok=True)

    print(f"Initialized Agent Harness in {project}")
    if written:
        print("Files written:")
        for path in written:
            print(f"- {path.relative_to(project)}")
    else:
        print("No files written; existing files were preserved. Use --force to overwrite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

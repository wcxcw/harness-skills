#!/usr/bin/env python3
"""Report project manifests and declared scripts without executing or changing them."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


SKIP_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".codex", ".venv", "venv", "node_modules",
    "vendor", "dist", "build", "target", "coverage", ".next", ".vite", ".cache",
    ".turbo", ".nuxt", ".output", ".pytest_cache", "__pycache__",
}
MANIFESTS = {
    "package.json": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "Pipfile": "python",
    "setup.py": "python",
    "pom.xml": "maven",
    "build.gradle": "gradle",
    "build.gradle.kts": "gradle",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "Gemfile": "ruby",
    "composer.json": "php",
    "Makefile": "make",
}
CI_FILES = {".gitlab-ci.yml", "Jenkinsfile", ".circleci/config.yml"}


def discover(root: Path, max_depth: int) -> dict:
    manifests: list[dict] = []
    scripts: list[dict] = []
    ci: list[dict] = []
    errors: list[dict] = []
    def on_error(exc: OSError) -> None:
        errors.append({"source": str(exc.filename or root), "error": type(exc).__name__})

    for current, dirs, files in os.walk(root, followlinks=False, onerror=on_error):
        directory = Path(current)
        relative = directory.relative_to(root)
        depth = len(relative.parts)
        dirs[:] = sorted(
            name for name in dirs
            if name not in SKIP_DIRS
            and not (directory.name == "harness" and name == "runs")
            and not (directory / name).is_symlink()
            and depth < max_depth
        )
        for name in sorted(files):
            path = directory / name
            if path.is_symlink():
                continue
            source = path.relative_to(root).as_posix()
            if name in MANIFESTS:
                manifests.append({"source": source, "ecosystem": MANIFESTS[name], "status": "Discovered"})
            if source in CI_FILES or (
                len(relative.parts) == 2 and relative.parts == (".github", "workflows")
                and path.suffix.lower() in {".yml", ".yaml"}
            ):
                ci.append({"source": source, "status": "Discovered"})
            if name != "package.json":
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append({"source": source, "error": type(exc).__name__})
                continue
            declared = data.get("scripts") if isinstance(data, dict) else None
            if not isinstance(declared, dict):
                continue
            for script_name, definition in sorted(declared.items()):
                if not isinstance(script_name, str) or not isinstance(definition, str):
                    continue
                scripts.append({
                    "source": source,
                    "working_directory": relative.as_posix(),
                    "script": script_name,
                    "status": "Discovered",
                    "verified": False,
                    "side_effects": "Not assessed",
                })
    return {
        "project": str(root),
        "max_depth": max_depth,
        "manifests": manifests,
        "package_scripts": scripts,
        "ci": ci,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="Project root to inspect without writing.")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum directory depth (default: 4).")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"Project directory not found: {root}")
    if not 0 <= args.max_depth <= 12:
        parser.error("--max-depth must be between 0 and 12")
    print(json.dumps(discover(root, args.max_depth), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

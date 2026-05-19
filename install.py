#!/usr/bin/env python3
"""Install the Harness skill pack into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def install_skill(src: Path, target_root: Path, force: bool) -> str:
    dst = target_root / src.name
    if dst.exists():
        if not force:
            return f"skipped existing {dst}"
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return f"installed {src.name} -> {dst}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Harness skills.")
    parser.add_argument("--target", default=str(default_target()), help="Codex skills directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing installed skills.")
    args = parser.parse_args()

    pack_root = Path(__file__).resolve().parent
    skills_root = pack_root / "skills"
    target = Path(args.target).expanduser().resolve()

    if not skills_root.exists():
        raise SystemExit(f"Missing skills directory: {skills_root}")

    target.mkdir(parents=True, exist_ok=True)

    for skill in sorted(skills_root.iterdir()):
        if skill.is_dir() and (skill / "SKILL.md").exists():
            print(install_skill(skill, target, args.force))

    print(f"Done. Installed skills directory: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

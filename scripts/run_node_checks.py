#!/usr/bin/env python3
"""Install locked Node dependencies and run repository-defined checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


CHECKS = ("format:check", "lint", "typecheck", "test", "build")


def run(command: list[str]) -> int:
    return subprocess.run(command, check=False).returncode


def commands_for_root(root: Path) -> tuple[list[str], list[str]]:
    if (root / "pnpm-lock.yaml").is_file():
        return ["pnpm", "install", "--frozen-lockfile"], ["pnpm", "run"]
    if (root / "yarn.lock").is_file():
        return ["yarn", "install", "--immutable"], ["yarn", "run"]
    if (root / "package-lock.json").is_file() or (
        root / "npm-shrinkwrap.json"
    ).is_file():
        return ["npm", "ci"], ["npm", "run"]
    raise FileNotFoundError("a supported lockfile is required")


def main() -> int:
    package = Path("package.json")
    if not package.is_file():
        print("node error: package.json is missing", file=sys.stderr)
        return 1
    payload = json.loads(package.read_text(encoding="utf-8"))
    scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
    try:
        install, command = commands_for_root(Path.cwd())
    except FileNotFoundError as error:
        print(f"node error: {error}", file=sys.stderr)
        return 1
    result = run(install)
    if result:
        return result
    for name in CHECKS:
        if name in scripts:
            result = run([*command, name])
            if result:
                return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

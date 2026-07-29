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


def main() -> int:
    package = Path("package.json")
    if not package.is_file():
        print("node error: package.json is missing", file=sys.stderr)
        return 1
    payload = json.loads(package.read_text(encoding="utf-8"))
    scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
    if Path("pnpm-lock.yaml").is_file():
        install = ["pnpm", "install", "--frozen-lockfile"]
        command = ["pnpm", "run"]
    elif Path("yarn.lock").is_file():
        install = ["yarn", "install", "--immutable"]
        command = ["yarn", "run"]
    elif Path("package-lock.json").is_file() or Path("npm-shrinkwrap.json").is_file():
        install = ["npm", "ci"]
        command = ["npm", "run"]
    else:
        print("node error: a supported lockfile is required", file=sys.stderr)
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

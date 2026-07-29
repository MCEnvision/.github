#!/usr/bin/env python3
"""Validate action publishers and immutable workflow references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


USES_PATTERN = re.compile(
    r"""^\s*(?:-\s*)?uses:\s*["']?([^"'#\s]+)["']?\s*(?:#.*)?$"""
)
FULL_SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
GITHUB_OWNED = {"actions", "github"}
AUDITED_REPOSITORIES = {
    "anchore/sbom-action",
    "gradle/actions",
    "MCEnvision/.github",
    "ossf/scorecard-action",
    "trufflesecurity/trufflehog",
}
SHARED_CODEQL_QUERY_ROOT = ".github-central/codeql/"


def workflow_files(root: Path) -> list[Path]:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return []
    return sorted([*workflows.rglob("*.yml"), *workflows.rglob("*.yaml")])


def repository_from_target(target: str) -> str:
    path = target.split("@", 1)[0]
    parts = path.split("/")
    if len(parts) < 2:
        return path
    if ".github/workflows/" in path:
        return "/".join(parts[:2])
    if parts[0].casefold() == "gradle" and parts[1].casefold() == "actions":
        return "gradle/actions"
    return "/".join(parts[:2])


def validate_target(target: str) -> str | None:
    if target.startswith("./"):
        return None
    if target.startswith("docker://"):
        return "container actions are not in the approved publisher policy"
    if "@" not in target:
        return "reference has no immutable revision"
    revision = target.rsplit("@", 1)[1]
    if not FULL_SHA_PATTERN.fullmatch(revision):
        return "reference is not pinned to a full 40 character commit sha"
    repository = repository_from_target(target)
    owner = repository.split("/", 1)[0]
    if owner in GITHUB_OWNED or repository in AUDITED_REPOSITORIES:
        return None
    return f"publisher is not approved, {repository}"


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for path in workflow_files(root):
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
        ):
            if (
                SHARED_CODEQL_QUERY_ROOT in line
                and f"./{SHARED_CODEQL_QUERY_ROOT}" not in line
            ):
                errors.append(
                    f"{relative}:{number}: shared CodeQL query paths must begin with ./"
                )
            if (
                relative == ".github/workflows/codeql.yml"
                and "scripts/run_gradle.py" in line
                and "--force-execution" not in line
            ):
                errors.append(
                    f"{relative}:{number}: CodeQL Gradle extraction must force execution"
                )
            match = USES_PATTERN.match(line)
            if not match:
                continue
            target = match.group(1)
            failure = validate_target(target)
            if failure:
                errors.append(f"{relative}:{number}: {target}, {failure}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"workflow policy error: {error}", file=sys.stderr)
        return 1
    print("workflow policy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

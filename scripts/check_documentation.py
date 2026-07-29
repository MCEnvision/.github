#!/usr/bin/env python3
"""Validate repository documentation structure, links, and change coverage."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path


LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
IMPLEMENTATION_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".py",
    ".rb",
    ".rs",
    ".swift",
    ".ts",
    ".tsx",
}
IMPLEMENTATION_NAMES = {
    "build.gradle",
    "build.gradle.kts",
    "gradle.properties",
    "package.json",
    "pom.xml",
    "pyproject.toml",
    "settings.gradle",
    "settings.gradle.kts",
}


def git_changed_files(base_sha: str) -> list[Path]:
    if not base_sha:
        return []
    process = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}...HEAD"],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        return []
    return [Path(line.strip()) for line in process.stdout.splitlines() if line.strip()]


def normalized_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith(("#", "mailto:", "http://", "https://")):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0]
    target = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    path = Path(target)
    return path if path.is_absolute() else source.parent / path


def validate(root: Path, enforce_layout: bool, base_sha: str) -> list[str]:
    errors: list[str] = []
    readme = root / "README.md"
    if not readme.is_file():
        errors.append("README.md is missing from the repository root")

    if enforce_layout:
        required = [
            root / "docs" / "README.md",
            root / "docs" / "general" / "documentation.md",
            root / "docs" / "general" / "plan.md",
        ]
        for path in required:
            if not path.is_file():
                errors.append(f"{path.relative_to(root).as_posix()} is missing")
        root_markdown = sorted(
            path.name
            for path in root.glob("*.md")
            if path.name.casefold() not in {"readme.md", "agents.md"}
        )
        if root_markdown:
            errors.append(
                "README.md must be the only root Markdown document, found "
                + ", ".join(root_markdown)
            )

    markdown_files = sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts
        and ".codegraph" not in path.parts
        and path.name.casefold() != "agents.md"
    )
    for source in markdown_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        for match in LINK_PATTERN.finditer(text):
            target = normalized_target(source, match.group(1))
            if target is not None and not target.exists():
                errors.append(
                    f"{source.relative_to(root).as_posix()} links to missing "
                    f"{target.resolve(strict=False)}"
                )

    changed = git_changed_files(base_sha)
    implementation_changed = any(
        path.suffix.casefold() in IMPLEMENTATION_SUFFIXES
        or path.name.casefold() in IMPLEMENTATION_NAMES
        or path.as_posix().startswith("src/")
        for path in changed
    )
    documentation_changed = any(
        path.name.casefold() == "readme.md"
        or path.as_posix().casefold().startswith("docs/")
        for path in changed
    )
    if implementation_changed and not documentation_changed:
        errors.append(
            "implementation changed without a matching README.md or docs update"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--enforce-layout", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root, args.enforce_layout, args.base_sha)
    if errors:
        for error in errors:
            print(f"documentation error: {error}", file=sys.stderr)
        return 1
    print("documentation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

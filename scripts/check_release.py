#!/usr/bin/env python3
"""Validate release artifacts and create deterministic checksum metadata."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path


def digest(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def artifacts(patterns: list[str]) -> list[Path]:
    found: set[Path] = set()
    for pattern in patterns:
        for value in glob.glob(pattern, recursive=True):
            path = Path(value)
            if path.is_file():
                found.add(path.resolve())
    return sorted(found)


def validate_archive(path: Path) -> str | None:
    if path.stat().st_size == 0:
        return "artifact is empty"
    if path.suffix.casefold() not in {".jar", ".zip"}:
        return None
    try:
        with zipfile.ZipFile(path) as archive:
            corrupt = archive.testzip()
            if corrupt:
                return f"archive contains a corrupt entry, {corrupt}"
            if not archive.namelist():
                return "archive contains no entries"
    except zipfile.BadZipFile:
        return "artifact is not a valid ZIP or JAR archive"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifact-glob",
        action="append",
        required=True,
        help="glob for expected release artifacts, repeatable",
    )
    parser.add_argument("--output-directory", type=Path, default=Path("release-validation"))
    args = parser.parse_args()

    selected = artifacts(args.artifact_glob)
    if not selected:
        print("release error: no artifacts matched the configured globs", file=sys.stderr)
        return 1

    failures = []
    records = []
    working_directory = Path.cwd().resolve()
    for path in selected:
        failure = validate_archive(path)
        if failure:
            failures.append(f"{path}: {failure}")
            continue
        records.append(
            {
                "path": path.relative_to(working_directory).as_posix(),
                "size": path.stat().st_size,
                "sha256": digest(path, "sha256"),
                "sha512": digest(path, "sha512"),
            }
        )
    if failures:
        for failure in failures:
            print(f"release error: {failure}", file=sys.stderr)
        return 1

    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "release-checksums.sha256").write_text(
        "".join(f"{record['sha256']}  {record['path']}\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )
    (output / "release-checksums.sha512").write_text(
        "".join(f"{record['sha512']}  {record['path']}\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "repository": os.environ.get("GITHUB_REPOSITORY", ""),
        "commit": os.environ.get("GITHUB_SHA", ""),
        "run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "artifacts": records,
    }
    (output / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"validated {len(records)} release artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

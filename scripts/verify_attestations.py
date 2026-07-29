#!/usr/bin/env python3
"""Verify release artifact attestations against the expected reusable workflow."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from scripts.check_release import artifacts
except ModuleNotFoundError:
    from check_release import artifacts


def verification_command(
    artifact: Path,
    repository: str,
    signer_repository: str,
    signer_workflow: str,
) -> list[str]:
    return [
        "gh",
        "attestation",
        "verify",
        "--repo",
        repository,
        "--signer-repo",
        signer_repository,
        "--signer-workflow",
        signer_workflow,
        str(artifact),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-glob", action="append", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--signer-repository", required=True)
    parser.add_argument("--signer-workflow", required=True)
    args = parser.parse_args()
    selected = artifacts(args.artifact_glob)
    if not selected:
        print("attestation error: no release artifacts matched", file=sys.stderr)
        return 1
    for artifact in selected:
        command = verification_command(
            artifact,
            args.repository,
            args.signer_repository,
            args.signer_workflow,
        )
        result = subprocess.run(command, check=False)
        if result.returncode:
            print(
                f"attestation error: verification failed for {artifact}",
                file=sys.stderr,
            )
            return result.returncode
    print(f"verified {len(selected)} release artifact attestations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

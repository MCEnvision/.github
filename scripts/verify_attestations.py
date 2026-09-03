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

PROVENANCE_PREDICATE = "https://slsa.dev/provenance/v1"
SPDX_PREDICATE = "https://spdx.dev/Document/v2.3"


def verification_commands(
    artifact: Path,
    repository: str,
    signer_workflow: str,
    source_digest: str,
) -> list[tuple[str, list[str]]]:
    commands = []
    for predicate in (PROVENANCE_PREDICATE, SPDX_PREDICATE):
        commands.append(
            (
                predicate,
                [
                    "gh",
                    "attestation",
                    "verify",
                    "--repo",
                    repository,
                    "--signer-workflow",
                    signer_workflow,
                    "--source-digest",
                    source_digest,
                    "--predicate-type",
                    predicate,
                    str(artifact),
                ],
            )
        )
    return commands


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-glob", action="append", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--signer-workflow", required=True)
    parser.add_argument("--source-digest", required=True)
    args = parser.parse_args()
    selected = artifacts(args.artifact_glob)
    if not selected:
        print("attestation error: no release artifacts matched", file=sys.stderr)
        return 1
    for artifact in selected:
        commands = verification_commands(
            artifact,
            args.repository,
            args.signer_workflow,
            args.source_digest,
        )
        for predicate, command in commands:
            result = subprocess.run(command, check=False)
            if result.returncode:
                print(
                    f"attestation error: {predicate} verification failed for {artifact}",
                    file=sys.stderr,
                )
                return result.returncode
    print(
        f"verified {len(selected)} release artifacts for provenance and SPDX SBOM attestations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

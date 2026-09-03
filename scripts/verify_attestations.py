#!/usr/bin/env python3
"""Verify release artifact attestations against the expected reusable workflow."""

from __future__ import annotations

import argparse
import shutil
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


def tampered_artifacts(selected: list[Path], output_directory: Path) -> list[Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    tampered = []
    for artifact in selected:
        target = output_directory / artifact.name
        shutil.copyfile(artifact, target)
        content = target.read_bytes()
        if not content:
            raise ValueError(f"Cannot tamper with empty artifact {artifact}")
        target.write_bytes(bytes([content[0] ^ 0xFF]) + content[1:])
        tampered.append(target)
    return tampered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-glob", action="append", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--signer-workflow", required=True)
    parser.add_argument("--source-digest", required=True)
    parser.add_argument("--expect-failure", action="store_true")
    parser.add_argument("--tamper-output-directory", type=Path)
    args = parser.parse_args()
    selected = artifacts(args.artifact_glob)
    if not selected:
        print("attestation error: no release artifacts matched", file=sys.stderr)
        return 1
    if args.tamper_output_directory:
        try:
            selected = tampered_artifacts(selected, args.tamper_output_directory)
        except (OSError, ValueError) as error:
            print(f"attestation error: could not create tampered artifacts. {error}", file=sys.stderr)
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
            if args.expect_failure and result.returncode == 0:
                print(
                    f"attestation error: {predicate} unexpectedly accepted {artifact}",
                    file=sys.stderr,
                )
                return 1
            if not args.expect_failure and result.returncode:
                print(
                    f"attestation error: {predicate} verification failed for {artifact}",
                    file=sys.stderr,
                )
                return result.returncode
    if args.expect_failure:
        print(
            f"verified {len(selected)} tampered release artifacts were rejected for provenance and SPDX SBOM attestations"
        )
        return 0
    print(
        f"verified {len(selected)} release artifacts for provenance and SPDX SBOM attestations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

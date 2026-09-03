import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.verify_attestations import (
    PROVENANCE_PREDICATE,
    SPDX_PREDICATE,
    main as verify_attestations,
    verification_commands,
)
from scripts.verify_release_tag import validate_tag


class ReleaseEvidenceValidationTest(unittest.TestCase):
    def test_verified_annotated_tag_passes(self) -> None:
        commit = "0123456789abcdef0123456789abcdef01234567"
        reference = {"object": {"type": "tag", "sha": "tag-object"}}
        tag = {
            "object": {"type": "commit", "sha": commit},
            "verification": {"verified": True, "reason": "valid"},
        }
        self.assertEqual(validate_tag(reference, tag, commit), [])

    def test_lightweight_or_unverified_tag_fails(self) -> None:
        commit = "0123456789abcdef0123456789abcdef01234567"
        reference = {"object": {"type": "commit", "sha": commit}}
        tag = {
            "object": {"type": "commit", "sha": commit},
            "verification": {"verified": False, "reason": "unsigned"},
        }
        errors = validate_tag(reference, tag, commit)
        self.assertTrue(any("not an annotated tag" in error for error in errors))
        self.assertTrue(any("not verified" in error for error in errors))

    def test_attestation_commands_pin_workflow_source_and_predicates(self) -> None:
        commands = verification_commands(
            Path("build/libs/example.jar"),
            "MCEnvision/example",
            "MCEnvision/.github/.github/workflows/release-validation.yml",
            "0123456789abcdef0123456789abcdef01234567",
        )
        self.assertEqual(
            [predicate for predicate, _ in commands],
            [PROVENANCE_PREDICATE, SPDX_PREDICATE],
        )
        for _, command in commands:
            self.assertEqual(command[0:3], ["gh", "attestation", "verify"])
            self.assertIn("MCEnvision/example", command)
            self.assertIn(
                "MCEnvision/.github/.github/workflows/release-validation.yml",
                command,
            )
            self.assertIn("0123456789abcdef0123456789abcdef01234567", command)
            self.assertNotIn("--signer-repo", command)

    def test_sbom_failure_fails_closed_after_provenance_succeeds(self) -> None:
        with TemporaryDirectory() as directory:
            artifact = Path(directory) / "example.jar"
            artifact.write_bytes(b"release artifact")
            arguments = [
                "verify_attestations.py",
                "--artifact-glob",
                str(artifact),
                "--repository",
                "MCEnvision/example",
                "--signer-workflow",
                "MCEnvision/.github/.github/workflows/release-validation.yml",
                "--source-digest",
                "0123456789abcdef0123456789abcdef01234567",
            ]
            with (
                patch.object(sys, "argv", arguments),
                patch(
                    "scripts.verify_attestations.subprocess.run",
                    side_effect=[
                        subprocess.CompletedProcess([], 0),
                        subprocess.CompletedProcess([], 1),
                    ],
                ) as run,
            ):
                self.assertEqual(verify_attestations(), 1)
            self.assertEqual(run.call_count, 2)
            second_command = run.call_args_list[1].args[0]
            self.assertEqual(
                second_command[second_command.index("--predicate-type") + 1],
                SPDX_PREDICATE,
            )


if __name__ == "__main__":
    unittest.main()

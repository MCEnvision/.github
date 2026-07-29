import unittest
from pathlib import Path

from scripts.verify_attestations import verification_command
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

    def test_attestation_command_pins_identity(self) -> None:
        command = verification_command(
            Path("build/libs/example.jar"),
            "MCEnvision/example",
            "MCEnvision/.github",
            "MCEnvision/.github/.github/workflows/release-validation.yml",
        )
        self.assertEqual(command[0:3], ["gh", "attestation", "verify"])
        self.assertIn("MCEnvision/example", command)
        self.assertIn("MCEnvision/.github", command)
        self.assertIn(
            "MCEnvision/.github/.github/workflows/release-validation.yml",
            command,
        )


if __name__ == "__main__":
    unittest.main()

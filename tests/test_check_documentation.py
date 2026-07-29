import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.check_documentation import validate


class DocumentationValidationTest(unittest.TestCase):
    def test_complete_layout_passes(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[Documentation](docs/README.md)\n", encoding="utf-8"
            )
            (root / "docs" / "general").mkdir(parents=True)
            (root / "docs" / "README.md").write_text(
                "[Documentation](general/documentation.md)\n", encoding="utf-8"
            )
            (root / "docs" / "general" / "documentation.md").write_text(
                "# Documentation\n", encoding="utf-8"
            )
            (root / "docs" / "general" / "plan.md").write_text(
                "# Plan\n", encoding="utf-8"
            )
            self.assertEqual(validate(root, True, ""), [])

    def test_missing_target_fails(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[Missing](docs/missing.md)\n", encoding="utf-8"
            )
            errors = validate(root, False, "")
            self.assertTrue(any("links to missing" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

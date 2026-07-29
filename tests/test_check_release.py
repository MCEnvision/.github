import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.check_release import artifacts, validate_archive


class ReleaseValidationTest(unittest.TestCase):
    def test_valid_jar(self) -> None:
        with TemporaryDirectory() as directory:
            jar = Path(directory) / "example.jar"
            with zipfile.ZipFile(jar, "w") as archive:
                archive.writestr("example.txt", "ok")
            self.assertIsNone(validate_archive(jar))

    def test_empty_artifact_fails(self) -> None:
        with TemporaryDirectory() as directory:
            jar = Path(directory) / "empty.jar"
            jar.write_bytes(b"")
            self.assertEqual(validate_archive(jar), "artifact is empty")

    def test_artifact_glob_is_sorted(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.jar").write_bytes(b"b")
            (root / "a.jar").write_bytes(b"a")
            result = artifacts([str(root / "*.jar")])
            self.assertEqual([path.name for path in result], ["a.jar", "b.jar"])


if __name__ == "__main__":
    unittest.main()

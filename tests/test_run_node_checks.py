import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.run_node_checks import commands_for_root


class NodeRunnerTest(unittest.TestCase):
    def test_pnpm_lockfile_selects_frozen_install(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pnpm-lock.yaml").write_text("", encoding="utf-8")
            install, command = commands_for_root(root)
            self.assertEqual(install, ["pnpm", "install", "--frozen-lockfile"])
            self.assertEqual(command, ["pnpm", "run"])

    def test_npm_lockfile_selects_ci(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package-lock.json").write_text("{}", encoding="utf-8")
            install, command = commands_for_root(root)
            self.assertEqual(install, ["npm", "ci"])
            self.assertEqual(command, ["npm", "run"])

    def test_missing_lockfile_fails(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "supported lockfile"):
                commands_for_root(Path(directory))


if __name__ == "__main__":
    unittest.main()

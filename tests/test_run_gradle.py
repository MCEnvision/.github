import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.run_gradle import parse_tasks, wrapper_command


class GradleRunnerTest(unittest.TestCase):
    def test_task_list_is_preserved(self) -> None:
        self.assertEqual(
            parse_tasks("spotlessCheck test build"),
            ["spotlessCheck", "test", "build"],
        )

    def test_shell_operators_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid task names"):
            parse_tasks("build && whoami")

    def test_gradle_options_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid task names"):
            parse_tasks("build --scan")

    def test_linux_wrapper_command(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
            wrapper, command = wrapper_command(["build"], root, "posix")
            self.assertEqual(wrapper, root / "gradlew")
            self.assertEqual(command, ["./gradlew", "--no-daemon", "build"])

    def test_forced_linux_wrapper_command(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
            wrapper, command = wrapper_command(
                ["check", "build"],
                root,
                "posix",
                force_execution=True,
            )
            self.assertEqual(wrapper, root / "gradlew")
            self.assertEqual(
                command,
                [
                    "./gradlew",
                    "--no-daemon",
                    "--no-build-cache",
                    "--rerun-tasks",
                    "check",
                    "build",
                ],
            )

    def test_forced_windows_wrapper_command(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            wrapper_path = root / "gradlew.bat"
            wrapper_path.write_text("@echo off\n", encoding="utf-8")
            wrapper, command = wrapper_command(
                ["build"],
                root,
                "nt",
                force_execution=True,
            )
            self.assertEqual(wrapper, wrapper_path)
            self.assertEqual(
                command,
                [
                    str(wrapper_path),
                    "--no-daemon",
                    "--no-build-cache",
                    "--rerun-tasks",
                    "build",
                ],
            )


if __name__ == "__main__":
    unittest.main()

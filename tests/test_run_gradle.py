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

    def test_linux_wrapper_command(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
            wrapper, command = wrapper_command(["build"], root, "posix")
            self.assertEqual(wrapper, root / "gradlew")
            self.assertEqual(command, ["./gradlew", "--no-daemon", "build"])


if __name__ == "__main__":
    unittest.main()

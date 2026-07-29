#!/usr/bin/env python3
"""Run an explicit, validated Gradle task list through the checked-in wrapper."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


TASK_PATTERN = re.compile(r"^[-:A-Za-z0-9._]+$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    args = parser.parse_args()
    tasks = shlex.split(args.tasks)
    if not tasks:
        print("gradle error: no tasks were configured", file=sys.stderr)
        return 1
    invalid = [task for task in tasks if not TASK_PATTERN.fullmatch(task)]
    if invalid:
        print(
            "gradle error: invalid task names, " + ", ".join(invalid),
            file=sys.stderr,
        )
        return 1
    wrapper = Path("gradlew.bat" if os.name == "nt" else "gradlew")
    if not wrapper.is_file():
        print("gradle error: checked-in Gradle Wrapper is missing", file=sys.stderr)
        return 1
    if os.name != "nt":
        wrapper.chmod(wrapper.stat().st_mode | 0o111)
        command = [f"./{wrapper.name}", "--no-daemon", *tasks]
    else:
        command = [str(wrapper), "--no-daemon", *tasks]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

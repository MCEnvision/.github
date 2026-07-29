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


def parse_tasks(value: str) -> list[str]:
    tasks = shlex.split(value)
    if not tasks:
        raise ValueError("no tasks were configured")
    invalid = [task for task in tasks if not TASK_PATTERN.fullmatch(task)]
    if invalid:
        raise ValueError("invalid task names, " + ", ".join(invalid))
    return tasks


def wrapper_command(
    tasks: list[str], root: Path, platform_name: str
) -> tuple[Path, list[str]]:
    wrapper = root / ("gradlew.bat" if platform_name == "nt" else "gradlew")
    if not wrapper.is_file():
        raise FileNotFoundError("checked-in Gradle Wrapper is missing")
    if platform_name == "nt":
        return wrapper, [str(wrapper), "--no-daemon", *tasks]
    return wrapper, [f"./{wrapper.name}", "--no-daemon", *tasks]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    args = parser.parse_args()
    try:
        tasks = parse_tasks(args.tasks)
        wrapper, command = wrapper_command(tasks, Path.cwd(), os.name)
    except (FileNotFoundError, ValueError) as error:
        print(f"gradle error: {error}", file=sys.stderr)
        return 1
    if os.name != "nt":
        wrapper.chmod(wrapper.stat().st_mode | 0o111)
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

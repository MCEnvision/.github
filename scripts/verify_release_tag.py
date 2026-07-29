#!/usr/bin/env python3
"""Verify that a release ref is an annotated tag with a valid GitHub signature."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse


def gh_api(path: str) -> dict:
    process = subprocess.run(
        ["gh", "api", path],
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or f"github api failed for {path}")
    payload = json.loads(process.stdout)
    if not isinstance(payload, dict):
        raise RuntimeError(f"github api returned an invalid payload for {path}")
    return payload


def validate_tag(
    reference: dict, tag: dict, expected_commit: str
) -> list[str]:
    errors: list[str] = []
    target = reference.get("object")
    if not isinstance(target, dict) or target.get("type") != "tag":
        errors.append("release ref is not an annotated tag")
    tagged_object = tag.get("object")
    if (
        not isinstance(tagged_object, dict)
        or tagged_object.get("type") != "commit"
        or tagged_object.get("sha") != expected_commit
    ):
        errors.append("annotated tag does not target the workflow commit")
    verification = tag.get("verification")
    if not isinstance(verification, dict) or verification.get("verified") is not True:
        reason = (
            verification.get("reason", "unknown")
            if isinstance(verification, dict)
            else "missing"
        )
        errors.append(f"annotated tag signature is not verified, {reason}")
    return errors


def main() -> int:
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    tag_name = os.environ.get("GITHUB_REF_NAME", "")
    commit = os.environ.get("GITHUB_SHA", "")
    if not repository or not tag_name or not commit:
        print("release tag error: required GitHub context is missing", file=sys.stderr)
        return 1
    encoded = urllib.parse.quote(tag_name, safe="")
    try:
        reference = gh_api(f"repos/{repository}/git/ref/tags/{encoded}")
        target = reference.get("object")
        if not isinstance(target, dict) or target.get("type") != "tag":
            errors = ["release ref is not an annotated tag"]
        else:
            tag = gh_api(f"repos/{repository}/git/tags/{target.get('sha', '')}")
            errors = validate_tag(reference, tag, commit)
    except (RuntimeError, ValueError) as error:
        print(f"release tag error: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"release tag error: {error}", file=sys.stderr)
        return 1
    print(f"verified signed annotated tag {tag_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.check_workflow_policy import validate, validate_target


SHA = "0123456789abcdef0123456789abcdef01234567"


class WorkflowPolicyValidationTest(unittest.TestCase):
    def test_approved_full_sha_passes(self) -> None:
        self.assertIsNone(validate_target(f"actions/checkout@{SHA}"))
        self.assertIsNone(validate_target(f"gradle/actions/setup-gradle@{SHA}"))
        self.assertIsNone(
            validate_target(
                f"MCEnvision/.github/.github/workflows/quality.yml@{SHA}"
            )
        )

    def test_tag_and_unknown_publisher_fail(self) -> None:
        self.assertIn(
            "full 40 character commit sha",
            validate_target("actions/checkout@v7") or "",
        )
        self.assertIn(
            "publisher is not approved",
            validate_target(f"unknown/example@{SHA}") or "",
        )

    def test_workflow_reports_file_and_line(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "quality.yml").write_text(
                "jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v7\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn(".github/workflows/quality.yml:4", errors[0])

    def test_local_codeql_query_requires_explicit_relative_path(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            workflow = workflows / "codeql.yml"
            workflow.write_text(
                "queries: security-extended,"
                ".github-central/codeql/neoforge/neoforge-security.qls\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("must begin with ./", errors[0])

            workflow.write_text(
                "queries: security-extended,"
                "./.github-central/codeql/neoforge/neoforge-security.qls\n",
                encoding="utf-8",
            )
            self.assertEqual(validate(root), [])

    def test_codeql_gradle_extraction_requires_forced_execution(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            workflow = workflows / "codeql.yml"
            workflow.write_text(
                "run: python .github-central/scripts/run_gradle.py "
                '--tasks "$GRADLE_TASKS"\n',
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("must force execution", errors[0])

            workflow.write_text(
                "run: python .github-central/scripts/run_gradle.py "
                '--tasks "$GRADLE_TASKS" --force-execution\n',
                encoding="utf-8",
            )
            self.assertEqual(validate(root), [])

    def test_obsolete_java_codeql_method_type_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            query_root = root / "codeql" / "neoforge"
            query_root.mkdir(parents=True)
            (query_root / "Example.ql").write_text(
                "import java\nfrom MethodAccess call select call\n",
                encoding="utf-8",
            )
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "repository-quality.yml").write_text(
                "steps:\n"
                f"  - uses: github/codeql-action/setup-codeql@{SHA}\n"
                "  - run: codeql query compile --check-only -- codeql/neoforge\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("MethodCall type", errors[0])

    def test_custom_query_pack_requires_compilation_coverage(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            query_root = root / "codeql" / "neoforge"
            query_root.mkdir(parents=True)
            (query_root / "Example.ql").write_text(
                "import java\nfrom MethodCall call select call\n",
                encoding="utf-8",
            )
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            workflow = workflows / "repository-quality.yml"
            workflow.write_text(
                "steps:\n"
                f"  - uses: github/codeql-action/setup-codeql@{SHA}\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("compile the complete query pack", errors[0])

            workflow.write_text(
                "steps:\n"
                "  - run: codeql query compile --check-only -- codeql/neoforge\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("install the pinned CodeQL CLI", errors[0])


if __name__ == "__main__":
    unittest.main()

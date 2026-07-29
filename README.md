# EnVisione Repository Standards

This repository provides shared GitHub Actions workflows and default community health files for EnVisione projects. Caller repositories keep only small event wrappers and repository-specific inputs. Build logic, security checks, documentation validation, and release verification stay centralized here.

## Shared Workflows

### Quality

`EnVisione/.github/.github/workflows/quality.yml@<reviewed commit sha>`

The quality workflow supports:

- Java toolchains with Java 21 as the default.
- Checked-in Gradle Wrapper validation and builds.
- Repository-selected GameTest tasks.
- Node.js validation when applicable.
- Nested Node.js project validation through an explicit working directory.
- Pull request dependency review for supported repositories.
- Documentation structure and internal-link validation.
- Secret scanning on pull requests, pushes, schedules, and manual runs.

### Privileged Security and Dependency Workflows

`EnVisione/.github/.github/workflows/codeql.yml@<reviewed commit sha>` runs CodeQL with `security-events: write` only for repositories and languages that support it.

`EnVisione/.github/.github/workflows/dependency-submission.yml@<reviewed commit sha>` submits the complete Gradle dependency graph with `contents: write` only after trusted default-branch pushes or manual runs.

### Release Validation

`EnVisione/.github/.github/workflows/release-validation.yml@<reviewed commit sha>`

The release workflow builds and inspects artifacts, creates SHA-256 and SHA-512 checksum files, generates an SPDX JSON SBOM, records the source commit, and creates build and SBOM attestations when GitHub supports them.

## Security Model

This public repository contains no credentials. Caller repositories retain credentials in branch-restricted GitHub environments. Reusable workflows receive only the permissions granted by the caller and do not inherit environment secrets.

External actions and caller references are pinned to full commit SHAs. The caller passes the same reviewed central commit to `shared-ref`, so validation scripts match the reusable workflow definition. Dependabot monitors external action references.

## Documentation

See the [documentation index](docs/README.md), [technical documentation](docs/general/documentation.md), and [implementation plan](docs/general/plan.md).

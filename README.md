# MCEnvision Repository Standards

This repository provides shared GitHub Actions workflows and default community health files for MCEnvision projects. Caller repositories keep only small event wrappers and repository specific inputs. Build logic, security checks, documentation validation, supply chain policy, and release verification stay centralized here.

## Shared Workflows

### Quality

`MCEnvision/.github/.github/workflows/quality.yml@<reviewed commit sha>`

The quality workflow supports:

- Java toolchains with Java 21 as the default.
- Checked-in Gradle Wrapper validation and builds.
- Repository-selected GameTest tasks.
- Node.js validation when applicable.
- Nested Node.js project validation through an explicit working directory.
- Pull request dependency review for supported repositories.
- Documentation structure and internal-link validation.
- Secret scanning on pull requests, pushes, and manual runs.
- Explicit job timeouts and seven day routine test evidence.
- Full commit SHA and approved publisher validation.

### Privileged Security and Dependency Workflows

`MCEnvision/.github/.github/workflows/codeql.yml@<reviewed commit sha>` runs CodeQL with `security-events: write` only for repositories and languages that support it. The security extended suite is always enabled. Applicable NeoForge callers also use the shared NeoForge query pack.

`MCEnvision/.github/.github/workflows/dependency-submission.yml@<reviewed commit sha>` submits the complete Gradle dependency graph with `contents: write` only after trusted default branch pushes or manual runs.

The shared repository scans its Python and GitHub Actions sources with CodeQL. OpenSSF Scorecard records public supply chain findings in the Security tab.

### Release Validation

`MCEnvision/.github/.github/workflows/release-validation.yml@<reviewed commit sha>`

The release workflow builds and inspects artifacts, creates SHA 256 and SHA 512 checksum files, generates an SPDX JSON SBOM, records the source commit, requires a verified signed annotated tag for tag initiated releases, and creates build and SBOM attestations when GitHub supports them. It then verifies the artifact digest and signer identity against the expected caller and shared workflow.

## Security Model

This public repository contains no credentials. Caller repositories retain credentials in branch-restricted GitHub environments. Reusable workflows receive only the permissions granted by the caller and do not inherit environment secrets.

External actions and caller references are pinned to full commit SHAs. The caller passes the same reviewed central commit to `shared-ref`, so validation scripts match the reusable workflow definition. Dependabot monitors external action references.

The central repository allows GitHub owned actions plus an audited list containing Gradle, TruffleHog, Anchore, and OpenSSF. GitHub also enforces full commit SHA pinning for this repository.

## GitHub Development Guidance

Organization custom agents live under `agents/`. Focused repository skills live under `.github/skills/` for NeoForge implementation, issue investigation, security review, releases, documentation, GameTests, and pull request auditing.

These files configure available guidance. They do not buy Copilot seats, enable metered automations, or invoke cloud agent work automatically.

## Cost Controls

MCEnvision uses hard zero dollar stop budgets for Actions, Codespaces, Packages, and Git LFS. Public standard Actions and public CodeQL remain available without paid minutes. Private repository workflows use included Team minutes and must use concurrency cancellation, timeouts, and short routine artifact retention.

Paid private code security, GitHub Code Quality, new organization seats, larger runners, Copilot seats or overages, and other metered capabilities require separate cost approval.

## Documentation

See the [documentation index](docs/README.md), [technical documentation](docs/general/documentation.md), and [implementation plan](docs/general/plan.md).

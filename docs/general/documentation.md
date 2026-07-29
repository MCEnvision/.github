# Technical Documentation

## Purpose

This repository is the shared implementation layer for GitHub validation across EnVisione repositories. Each caller repository defines when checks run and passes repository-specific inputs. The called workflows own the actual implementation.

## Workflow Topology

### Quality Workflow

The quality workflow is callable through `workflow_call`. Its read-only jobs are intentionally independent so GitHub reports precise check names and unrelated ecosystems can skip cleanly.

Callers pin the reusable workflow to a reviewed central commit and pass that same commit through `shared-ref`. Every shared script checkout therefore matches the workflow definition that selected it.

The Gradle job:

1. Checks out the caller repository.
2. Selects the configured Java toolchain.
3. Validates and configures the checked-in Gradle Wrapper.
4. Runs the repository-selected verification tasks.
5. Runs configured GameTest tasks when present.
6. Uploads test reports on failure.

The dependency review job runs only for pull requests when native dependency review is available. Public repositories support it. Private repositories owned by a personal account require a compatible GitHub Code Security plan and must leave the job disabled otherwise.

The documentation job runs when the caller enables `enforce-docs-layout`. It validates the root README, required documentation files, internal Markdown links, and documentation updates accompanying implementation changes. Migration callers may leave it disabled until repository onboarding has established the required documentation layout.

The secret scan uses a pinned TruffleHog release and reports verified and unknown findings. GitHub secret scanning and push protection remain separate native repository controls.

### Privileged Workflows

GitHub validates the complete permission graph of a reusable workflow before it evaluates job conditions. A skipped job cannot request permissions that its caller did not grant. Dependency submission and CodeQL therefore use dedicated reusable workflows instead of sharing the read-only quality workflow.

The dependency submission workflow runs only from a caller job gated to a trusted default-branch push or manual dispatch. It receives `contents: write` and submits Gradle's resolved dependency graph, including transitive dependencies.

The CodeQL workflow runs only when native code scanning is available and the caller supplies supported languages. It receives `security-events: write` without repository content write access. Public repositories support it. Private personal repositories on GitHub Pro do not receive native CodeQL unless their plan changes. Manual Gradle extraction receives a larger heap and runs Kotlin compilation in process to avoid instrumentation overhead exhausting the runner.

### Release Validation Workflow

Release validation uses a protected GitHub environment selected by the caller. It:

1. Builds with the caller's pinned Java and Gradle configuration.
2. Locates expected release artifacts.
3. Rejects empty or corrupt JAR files.
4. Produces SHA-256 and SHA-512 checksum inventories.
5. Records the source repository, commit, artifact size, and digest in a release manifest.
6. Generates an SPDX JSON SBOM.
7. Uploads a validation bundle.
8. Creates build provenance and SBOM attestations for public repositories.

GitHub Pro supports artifact attestations for public repositories. Private repositories require GitHub Enterprise Cloud, so private callers retain the checksums, manifest, SBOM, and workflow evidence without attempting unsupported attestations.

## Caller Contract

A caller workflow grants only the permissions needed by enabled jobs. The central workflow cannot elevate those permissions.

The standard caller supplies:

- The immutable shared workflow and script commit.
- Java version.
- Gradle verification tasks.
- Optional GameTest tasks.
- Whether Gradle and Node.js jobs apply, plus the Node.js working directory when the locked project is nested.
- Supported CodeQL languages.
- Whether native security features are available.
- Documentation layout enforcement.
- Optional dependency package and license restrictions.

Caller workflows must not pass publication credentials to the quality workflow. Release credentials belong in separate `curseforge`, `modrinth`, or `production` environments and are available only to jobs that explicitly reference those environments.

The baseline quality call receives read access only. A separate CodeQL call receives `security-events: write` only when supported languages are enabled. A separate dependency submission call receives `contents: write` only on trusted default-branch pushes or manual runs. Disabled capabilities do not appear in the caller permission graph.

## Branch and Merge Controls

Repositories use a branch ruleset targeting the default branch. It blocks deletion, force pushes, and direct updates that do not enter through a pull request. Pull request conversations must be resolved, but no human approval count is required.

Stable quality checks become required only after the caller workflow exists and its exact check names have completed successfully. This prevents a new or empty repository from being locked by a check that GitHub has never observed.

CODEOWNERS requests EnVisione review without making that review a merge requirement.

When Copilot code review is available, the ruleset requests review for new pull requests and new pushes. Copilot comments do not count as required approvals. Findings are evaluated against code, tests, repository rules, and current documentation before they are accepted or rejected.

## Environments

Source repositories receive a `testing` environment. Releasable repositories additionally receive `curseforge`, `modrinth`, and `production`.

Environment branch and tag policies limit access:

- `testing` accepts the default branch, phase branches under `envy/`, Dependabot branches, and pull request merge refs when repository testing requires an environment.
- `curseforge`, `modrinth`, and `production` accept the protected default branch and version tags.

No required human reviewer is configured. The branch, tag, ruleset, and workflow gates provide the automated approval path EnVy requested.

## Planning and Feedback

Every repository-scoped task begins with a quiet read-only preflight. It checks plan alignment, issues, pull requests, review threads, Copilot feedback, failed or pending checks, Actions state, Dependabot, security alerts, Project fields, milestones, wiki state, releases, rulesets, environments, and documentation drift.

Actionable feedback is verified before implementation. Valid findings update the plan, issue, Project item, implementation, tests, and documentation. Incorrect or inapplicable findings receive an evidence-based resolution. No feedback is silently accepted, silently ignored, or treated as a replacement for deterministic verification.

## Fleet Workflow Migration

Existing active repositories migrate through signed draft pull requests on `envy/central-workflow-migration`. The migration runs from temporary clones, so active local worktrees and phase branches remain untouched.

Each migration replaces copied generic build and CodeQL workflows with thin callers. Repository-specific smoke tests, schema validation, publication, deployment, and other custom workflows remain in place. A repository with the standard documentation tree enables documentation enforcement immediately. A legacy repository keeps that check disabled until its documentation is migrated without mixing unrelated file movement into the workflow pull request.

Caller generation detects a root or nested locked Node.js project. It enables Node.js validation only when both `package.json` and a supported lockfile exist, and passes the containing directory to the shared workflow.

The current rollout covers 29 eligible repositories. The central workflow repository, CodexGateway, the EnVisione profile repository, and the GitHub Pages repository remain outside this migration.

## Capability Boundaries

- Dependency review and native CodeQL are available for public repositories and compatible licensed private repositories.
- Artifact attestations are available for public repositories on GitHub Pro. Private attestations require GitHub Enterprise Cloud.
- GitHub environment branch and tag restrictions are available for private repositories on GitHub Pro.
- Copilot automatic review requires the pull request author to have access to Copilot review and available premium-request capacity.
- Native secret scanning and push protection are enabled where the repository plan supports them. The central secret scan remains active regardless.

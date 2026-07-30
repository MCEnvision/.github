# Technical Documentation

## Purpose

This repository is the shared implementation layer for GitHub validation across MCEnvision repositories. Each caller repository defines when checks run and passes repository specific inputs. The called workflows own the actual implementation.

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

Every job has an explicit timeout. Routine Gradle test evidence is retained for seven days. Event caller workflows cancel superseded pull request runs for the same branch.

### Privileged Workflows

GitHub validates the complete permission graph of a reusable workflow before it evaluates job conditions. A skipped job cannot request permissions that its caller did not grant. Dependency submission and CodeQL therefore use dedicated reusable workflows instead of sharing the read-only quality workflow.

The dependency submission workflow runs only from a caller job gated to a trusted default-branch push or manual dispatch. It receives `contents: write` and submits Gradle's resolved dependency graph, including transitive dependencies.

The CodeQL workflow runs only when native code scanning is available and the caller supplies supported languages. It receives `security-events: write` without repository content write access. Public repositories support it without paid minutes. Private repositories leave native code scanning disabled unless the existing organization entitlement supports it without additional charges. Manual Gradle extraction receives a larger heap and runs Kotlin compilation in process to avoid instrumentation overhead exhausting the runner. It invokes the validated Gradle runner with `--force-execution`, which adds `--no-build-cache` and `--rerun-tasks` internally. This guarantees that CodeQL observes compiler execution even when setup restores Gradle caches. Ordinary quality builds retain caching, and caller supplied task strings still cannot inject Gradle options.

CodeQL always runs the security extended suite. Applicable NeoForge callers additionally load the versioned query pack from `codeql/neoforge`. The reusable workflow checks out this repository beneath the caller and references the suite through the explicit local path `./.github-central/codeql/neoforge/neoforge-security.qls`. Central policy validation rejects the path without its `./` prefix because CodeQL would otherwise interpret it as an external repository specifier. The pack checks dedicated server client references, direct command permission gates, visible packet authority and thread validation, explicit network string bounds, and parameter flow into filesystem path resolution. These focused checks supplement GitHub standard queries and require repository evidence before a finding is accepted. The central quality workflow installs the CodeQL CLI through the pinned setup action, resolves the custom pack dependencies, and runs `query compile --check-only --keep-going` over the entire pack. This compilation gate catches incompatible QL types and predicates before any caller is repinned. Central policy validation also requires every `path-problem` query to import its flow module's `PathGraph`, which supplies the edge relation required when CodeQL interprets results as SARIF paths.

The shared repository analyzes its own Python and GitHub Actions sources. OpenSSF Scorecard runs against the public default branch and uploads SARIF to code scanning.

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
9. Verifies each public artifact attestation against the caller repository, `MCEnvision/.github`, the release validation workflow, and the artifact digest.

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

Automatic paid review is disabled. It is not a deterministic merge gate and must not consume a paid seat or repeatedly spend a limited review quota after pushes. A ready pull request may receive one review through the configured repository integration after local verification and required checks pass. Another review is requested only when a material implementation change invalidates the completed review. Review availability remains nonblocking, while formatting, tests, builds, CodeQL, dependency review, secret scanning, and repository specific acceptance checks remain authoritative.

The review path does not install a metered API key workflow and does not depend on an application gateway. It uses the configured repository integration and existing entitlement when available.

## Environments

Source repositories receive a `testing` environment. Releasable repositories additionally receive `curseforge`, `modrinth`, and `production`.

Environment branch and tag policies limit access:

- `testing` accepts the default branch, phase branches under `envy/`, Dependabot branches, and pull request merge refs when repository testing requires an environment.
- `curseforge`, `modrinth`, and `production` accept the protected default branch and version tags.

No required human reviewer is configured. The branch, tag, ruleset, and workflow gates provide the automated approval path EnVy requested.

## Planning and Feedback

Every repository-scoped task begins with a quiet read-only preflight. It checks plan alignment, issues, pull requests, review threads, Copilot feedback, failed or pending checks, Actions state, Dependabot, security alerts, Project fields, milestones, wiki state, releases, rulesets, environments, and documentation drift.

Actionable feedback is verified before implementation. Valid findings update the plan, issue, Project item, implementation, tests, and documentation. Incorrect or inapplicable findings receive an evidence-based resolution. No feedback is silently accepted, silently ignored, or treated as a replacement for deterministic verification.

## Actions Policy and Cost Controls

The central repository requires full commit SHA pinning and permits only GitHub owned actions plus audited Gradle, TruffleHog, Anchore, and OpenSSF repositories. `scripts/check_workflow_policy.py` independently validates every tracked workflow reference and rejects unknown publishers, tags, branches, and shortened revisions.

The organization remains on GitHub Team with two existing members and no outside collaborators. Hard zero dollar budgets stop further metered Actions, Codespaces, Packages, and Git LFS use. Repository transfer does not add a seat. Adding an organization member or outside collaborator to private repositories can add a seat and remains outside automatic onboarding.

Public standard Actions and public CodeQL do not consume paid minutes. Private repository workflows consume included Team minutes. Their event callers use per branch concurrency cancellation, explicit timeouts, path aware execution, and short routine retention. Paid private code security, GitHub Code Quality, Copilot seats or overages, larger runners, and any other paid capability remain disabled without explicit cost approval.

Custom secret patterns require GitHub Secret Protection for organization repositories. They are documented but not enabled because the zero additional spend constraint takes priority.

All Actions usage observed during the organization rollout was fully discounted or covered by included usage, leaving a net Actions charge of zero dollars. The same audit found approximately $1.23 of Secret Protection usage that had already accrued on private repositories. Secret Protection, private push protection, and private advanced security were disabled on every private repository. Hard zero dollar budgets with further usage blocked remain active for Actions, Codespaces, Packages, and Git LFS. The historical Secret Protection amount remains visible in billing until GitHub removes it or applies a credit.

## GitHub Copilot Configuration

Organization custom agents under `agents/` cover NeoForge implementation, issue investigation, security review, releases, documentation, GameTests, and pull request auditing. Repository skills under `.github/skills/` provide focused procedures for the same work.

The files are passive configuration. They do not grant repository permissions, buy seats, or trigger cloud agent runs. Copilot execution remains entitlement aware and user initiated.

## Fleet Workflow Migration

Existing active repositories migrate through signed draft pull requests on `envy/central-workflow-migration`. The migration runs from temporary clones, so active local worktrees and phase branches remain untouched.

Each migration replaces copied generic build and CodeQL workflows with thin callers. Repository-specific smoke tests, schema validation, publication, deployment, and other custom workflows remain in place. A repository with the standard documentation tree enables documentation enforcement immediately. A legacy repository keeps that check disabled until its documentation is migrated without mixing unrelated file movement into the workflow pull request.

Caller generation detects a root or nested locked Node.js project. It enables Node.js validation only when both `package.json` and a supported lockfile exist, and passes the containing directory to the shared workflow.

The historical caller rollout covered 29 repositories before the organization transfer. The current Minecraft fleet uses MCEnvision ownership. Unrelated personal repositories, the separate gateway integration, the EnVisione profile repository, and the GitHub Pages repository remain outside the organization migration.

### Rollout Result

The current organization rollout covers 25 transferred caller repositories. Thirteen migration pull requests passed their repository checks, received an approving assessment, had all review conversations resolved, and merged through the normal protected branch path.

The four major action upgrades were independently reviewed, tested, and merged before fleet rollout. The central workflows use `actions/setup-node` 7.0.0, `actions/checkout` 7.0.1, `actions/dependency-review-action` 5.0.0, and `actions/upload-artifact` 7.0.1 at audited full commit SHAs.

The thirteen passing caller repositories were repinned through verified pull requests. Twelve migration pull requests remain drafts with automatic merge disabled because their repository checks exposed project specific failures. Every transferred caller's default branch or active pull request head references the reviewed shared workflow commit `d731214d860ad2422ab8956a5d337dfaec51f64a`. A later documentation only commit in this repository does not change the reviewed workflow revision and does not require caller repinning. Transferred Minecraft pull requests resolve under MCEnvision through GitHub transfer redirects. Unrelated personal repositories remain under EnVisione.

No held repository was merged. Repairing one of these repositories requires its own scoped change, successful checks, resolved review feedback, and a fresh merge decision.

## Capability Boundaries

- Dependency review and native CodeQL are available for public repositories and compatible licensed private repositories.
- Artifact attestations are available for public repositories on GitHub Pro. Private attestations require GitHub Enterprise Cloud.
- GitHub environment branch and tag restrictions are available for private repositories on GitHub Pro.
- Copilot automatic review requires the pull request author to have access to Copilot review and available premium-request capacity.
- Native secret scanning and push protection are enabled where the repository plan supports them. The central secret scan remains active regardless.
- Organization custom secret patterns require GitHub Secret Protection and remain disabled under the zero additional spend policy.
- Merge queues are available only where the current repository visibility and organization plan support them. They are not a universal required gate.
- GitHub Code Quality and native coverage rules are not enabled because they can require a separately billed capability.
- The central release validation job records its selected GitHub environment. GitHub Release, CurseForge, Modrinth, staging, and production publication records must be emitted by the separate release broker because it owns the external upload result. That integration remains outside this repository while gateway work is excluded.

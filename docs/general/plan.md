# Implementation Plan

## Phase 1. Shared Workflow Foundation

- [x] Create the public, credential-free shared workflow repository.
- [x] Define the quality and release validation contracts.
- [x] Add deterministic validation scripts.
- [x] Validate the workflows in GitHub Actions.
- [x] Publish the verified initial baseline.

## Phase 2. Onboarding Integration

- [x] Replace copied CI and security workflows with thin shared-workflow callers.
- [x] Detect repository Java, Gradle, Node.js, GameTest, documentation, and CodeQL inputs.
- [x] Add rulesets, CODEOWNERS, environments, secret scanning, immutable releases, and supported attestations to onboarding.
- [x] Add signed commit and signed annotated tag requirements.
- [x] Add capability-aware fallback behavior that never creates permanently failing checks.

## Phase 3. Fleet Rollout

- [x] Apply supported remote settings to owned active repositories.
- [x] Preserve local worktrees, active phase branches, forks, archives, and excluded repositories. Include example repositories only when they are explicitly placed in rollout scope.
- [x] Open signed draft caller workflow migration pull requests for all 25 transferred caller repositories. Preserve repository specific verification and replace only copied generic workflows.
- [x] Reconcile migration pull request review findings before merge.
  - Pin every reusable workflow call and its shared validation scripts to one reviewed central commit.
  - Isolate dependency submission and CodeQL into dedicated reusable workflows so skipped privileged jobs cannot elevate a read-only caller during workflow validation.
  - Grant write permissions only to trusted default-branch and manual runs.
  - Grant pull request validation the minimum read and security permissions required by enabled jobs.
  - Detect nested Node.js projects and run their locked checks from the correct working directory.
  - Omit disabled or default-only inputs so caller intent remains clear.
  - Preserve repository-specific smoke, schema, deployment, and release checks when they exceed the shared baseline.
- [x] Merge only migration pull requests with completed successful checks, no requested changes, no unresolved actionable feedback, and a mergeable head. Thirteen migration pull requests met the gate and merged.
- [x] Leave repositories with existing build, test, dependency, wrapper, or lint failures open for repository-specific repair. Twelve migration pull requests remain draft with automatic merge disabled.
- [x] Verify zero remote drift after rollout.

## Phase 4. Continuous Reconciliation

- [x] Check all GitHub layers quietly at the start of every repository-scoped request.
- [x] Reconcile actionable review, security, dependency, CI, issue, Project, milestone, wiki, and release feedback.
- [x] Keep plans and canonical documentation synchronized with verified implementation.

## Phase 5. Organization Migration and Cost Guardrails

### Objective

Move the Minecraft repository fleet to the paid `MCEnvision` Team organization without adding seats or enabling metered overages. Preserve repository identity, pull requests, issues, releases, settings, redirects, and local worktrees.

### Completed Migration

- [x] Audit organization membership, collaborators, plan, billing budgets, repository visibility, forks, and name collisions before transfer.
- [x] Transfer the shared workflow repository and 24 Minecraft repositories from `EnVisione` to `MCEnvision`.
- [x] Verify all 25 transferred repository identities and GitHub redirects.
- [x] Update the Windows shared workflow clone and all 12 discovered node1 clones that still referenced the former owner.
- [x] Update repository onboarding so Minecraft repositories resolve under `MCEnvision`, while unrelated personal repositories remain under `EnVisione`.
- [x] Update missing Git behavior to search both the current organization and legacy redirects before creating a private repository under `MCEnvision`.
- [x] Record the ownership, remote reconciliation, and no duplicate repository rules in persistent operating context.

### Cost Constraints

- [x] Verify the organization remains on GitHub Team with two existing members and no outside collaborators.
- [x] Verify hard zero dollar budgets with further usage blocked for Actions, Codespaces, Packages, and Git LFS.
- [ ] Add a recurring read only billing and usage audit that reports approaching included limits without changing budgets or purchasing capacity.
- [x] Keep standard public repository Actions and public CodeQL enabled because they do not consume paid minutes.
- [x] Conserve private repository included Actions minutes with path filters, per branch concurrency cancellation, explicit timeouts, and short routine artifact retention.
- [x] Keep paid private repository code security, GitHub Code Quality, Copilot seats or overages, larger runners, additional organization seats, and other metered features disabled without explicit cost approval.
- [x] Disable Secret Protection and push protection on every private organization repository after the billing audit detected unintended licensed usage.

### Acceptance Criteria

- Every transferred repository resolves under `MCEnvision`, and every discovered clone uses the new remote.
- No repository is duplicated when a local project lacks `.git`.
- Transfer and workflow migration add no organization member, outside collaborator, or metered Actions overage.
- No further paid private security usage accrues after remediation. The billing record retains approximately $1.23 of Secret Protection usage incurred before the feature was disabled.
- Hard zero dollar budgets remain enabled and continue blocking further metered usage.

## Phase 6. Cost Safe Supply Chain Hardening

### Actions Policy and Workflow Resources

- [x] Require full commit SHA pinning in the shared repository and, where authorization allows, across the organization.
- [x] Restrict Actions to GitHub owned actions and an audited allowlist for Gradle, TruffleHog, Anchore, and OpenSSF.
- [x] Reject unpinned reusable workflows and unknown action publishers during central validation.
- [x] Add per branch concurrency cancellation to event caller workflows.
- [x] Add explicit job timeouts to every reusable workflow job.
- [x] Retain routine test evidence for seven days and release evidence for thirty days.
- [x] Remove the weekly central validation schedule. Dependabot retains its weekly update schedule, while code and security validation remain event driven.

### Central Repository Self Verification

- [x] Add Python and GitHub Actions CodeQL with the security extended query suite.
- [x] Add focused unit tests for Gradle task parsing, Node.js package manager selection, workflow policy validation, and release verification.
- [x] Add OpenSSF Scorecard for the public shared repository and publish its SARIF result to the Security tab.
- [x] Keep every external action at an individually reviewed full commit SHA.
- [x] Audit the four pending major action upgrades independently before merging any upgrade.

### NeoForge Security Queries

- [x] Add a versioned CodeQL query pack for NeoForge repositories.
- [x] Detect client classes entering common initialization or dedicated server paths.
- [x] Detect packet handlers that mutate state without validating logical side, sender, bounds, entity or level availability, or thread context.
- [x] Detect commands that perform privileged mutations without an explicit permission requirement.
- [x] Detect untrusted filesystem paths and traversal into configuration or generated data writes.
- [x] Detect hazardous serialization and network values with missing size or range bounds.
- [x] Run the custom pack only for applicable Java and NeoForge callers, alongside GitHub security extended queries.

### Release Integrity

- [x] Add protected version and phase tag rulesets that block deletion, replacement, and unsigned creation.
- [x] Require release validation to verify an annotated signed tag for tag initiated releases.
- [x] Verify artifact attestations against the expected owner, repository, reusable workflow, source commit, and digest before external upload.
- [ ] Record GitHub Release, CurseForge, Modrinth, staging, and production publication as GitHub Deployments with artifact digest, target version, environment, result, and rollback relationship. Central validation already records its selected GitHub environment. Target publication records belong to the separate release broker and remain deferred while gateway work is excluded.
- [x] Preserve checksums, source commit manifest, SPDX SBOM, and attestation evidence for every supported release.

### GitHub Native Development Guidance

- [x] Add organization level GitHub Copilot skills for NeoForge implementation, issue investigation, security review, release preparation, documentation, GameTests, and pull request auditing.
- [x] Add corresponding GitHub Copilot custom agents with least privilege tool access and evidence based completion gates.
- [x] Store the shared skills and agents in this organization `.github` repository so member repositories inherit them.
- [x] Do not purchase Copilot seats or invoke metered cloud agent work automatically. Configuration may be present while execution remains user initiated and entitlement aware.

### Secrets, Apps, and Runners

- [ ] Add audited custom secret patterns for Modrinth, CurseForge, Discord, Cloudflare, database URLs, and release broker credentials where the organization plan supports them without an added charge.
- [ ] Dry run every custom pattern against repository history before enabling push protection.
- [ ] Define GitHub App authentication for the separate gateway integration with signed webhook verification, short lived installation tokens, per repository permissions, idempotent delivery processing, and a failed delivery replay queue.
- [x] Keep gateway implementation changes separate while its active update is in progress.
- [x] Document an optional ephemeral node1 runner that is private repository only, single job, isolated, and wiped after each job.
- [x] Never dispatch public repository or fork pull request code to node1.

### Fleet Rollout

- [x] Merge the shared hardening pull request only after local checks, GitHub Actions, CodeQL, Scorecard, secret scanning, and available review findings are resolved.
- [x] Pin every caller to the reviewed shared merge commit.
- [x] Update transferred migration pull requests and open deduplicated migration pull requests for remaining caller drift.
- [x] Merge only callers whose required checks pass. Keep repositories with preexisting failures open for scoped repair.
- [x] Verify final organization ownership, caller revisions, Actions policies, tag rulesets, environments, security state, Projects, milestones, wiki links, and billed usage.

### Post Merge Rollout Correction

#### Current Evidence

The first organization caller rollout exposed four shared CodeQL configuration defects. NeoForge callers originally passed `.github-central/codeql/neoforge/neoforge-security.qls` as a query specifier. Without a leading `./`, CodeQL interpreted the value as an external repository specifier and stopped during database initialization before analysis began. After correcting that path, Java callers with otherwise successful Gradle builds showed a second failure. Gradle restored compilation output from cache, so the manually traced CodeQL build observed no compiler execution and failed database finalization with `CodeQL could not process any code written in Java/Kotlin`. Forced compilation corrected extraction and exposed a third defect during query compilation. Four custom NeoForge queries used the unresolved `MethodAccess` type instead of the current Java CodeQL `MethodCall` type. After type-correct queries compiled and executed, SARIF interpretation exposed a fourth defect. The path query did not import `PathFlow::PathGraph`, so its result metadata had no required edge relation. These failures are independent of caller source behavior.

#### Objective and Scope

- [x] Correct the shared NeoForge query suite reference to an explicit repository local path.
- [x] Extend central workflow policy validation and tests so a local CodeQL query suite cannot lose its `./` prefix without failing verification.
- [x] Add a dedicated forced execution mode to the validated Gradle runner. Use it only for manual CodeQL extraction to disable the build cache and rerun configured tasks without accepting arbitrary caller supplied Gradle options.
- [x] Test normal cached command construction and forced CodeQL command construction on Linux and Windows.
- [x] Replace unresolved Java CodeQL method access types with the supported `MethodCall` API while preserving each query's matching behavior.
- [x] Add a central query pack compilation job that installs the pinned CodeQL CLI, resolves the custom pack dependencies, and runs `query compile --check-only` on every custom query before caller rollout.
- [x] Extend central validation tests so the obsolete `MethodAccess` type and removal of query compilation coverage fail verification.
- [x] Import the generated path graph in every `path-problem` query so CodeQL produces the edge relation required for SARIF path interpretation.
- [x] Extend central validation tests so a path query without its flow module's `PathGraph` import fails before rollout.
- [x] Verify the repair with the central Python test suite, workflow policy validator, documentation validator, release validator, and GitHub Actions.
- [x] Merge the repair through a reviewed pull request, then repin each still open caller migration pull request to the repaired merge commit.
- [x] Reevaluate every caller after repinning. Merge only callers with successful deterministic checks, no requested changes, no unresolved actionable feedback, and a mergeable head.

#### Non Goals and Failure Handling

- Do not weaken CodeQL, disable the NeoForge query pack, bypass a failed check, or merge a repository with an unrelated build or test failure.
- Do not disable caching for ordinary quality builds. Forced execution is limited to CodeQL extraction.
- Do not remove or disable the custom NeoForge query pack to make caller checks pass.
- Do not change Minecraft, NeoForge, Gradle, mappings, dependencies, or repository implementation merely to complete the workflow migration.
- Keep repositories with independent failures in draft with automatic merge disabled. Record their exact failing gate for a later scoped repair.

#### Acceptance Criteria

- NeoForge CodeQL jobs resolve the shared query suite as a local path and complete initialization.
- Every custom NeoForge query compiles against the CodeQL Java library version installed by the pinned action.
- Every `path-problem` query provides a path graph and can be interpreted as SARIF after execution.
- Central validation rejects the broken path form.
- Every caller is pinned to one reviewed central merge commit.
- Only fully passing caller pull requests merge.
- Organization hard zero dollar budgets remain enabled, no Actions overage is introduced, and no further paid private security usage accrues after remediation.

## Phase 7. Fleet Repair and Repository Review

### Current Evidence

Twelve workflow migration pull requests remain draft because repository specific dependency, Gradle Wrapper, compilation, test, or CodeQL gates fail. Each pull request also accumulated six unsuccessful GitHub Copilot review attempts. The organization ruleset requested reviews for draft pull requests and requested another review after every push, which exhausted the available Copilot quota without producing useful findings.

### Review Policy

- Remove automatic GitHub Copilot review from organization repository rulesets and future onboarding.
- Do not purchase Copilot seats, enable Copilot overages, or make Copilot availability a merge requirement.
- Use one configured repository review after a pull request is ready and deterministic verification has passed.
- Do not request another review unless a material implementation change invalidates the completed review.
- Keep formatting, tests, builds, CodeQL, dependency review, secret scanning, and repository specific checks as the authoritative merge gates.
- Allow review unavailability to remain nonblocking when all deterministic required checks and repository acceptance criteria pass.
- Do not add a metered API key workflow merely to perform pull request review. Review must use the configured repository integration and existing entitlement.

### Repair Scope

- Reconcile every migration branch with the latest default branch before diagnosing a remaining failure.
- Repair repository specific dependency resolution, wrapper, source compatibility, test, and CodeQL failures without weakening required checks.
- Preserve repository architecture, supported Minecraft and loader versions, dependency boundaries, and existing user behavior unless a verified defect requires a scoped correction.
- Update each pull request with concise evidence of the repair and its verification result.
- Move a pull request out of draft only after its local verification and required GitHub checks pass.
- Merge each passing pull request through GitHub using a merge commit, then verify the resulting default branch.
- Keep any pull request open with its exact remaining blocker when a safe repository grounded repair cannot be completed.

### Acceptance Criteria

- Automatic Copilot review is absent from every owned organization repository ruleset and from repository onboarding.
- No pull request receives repeated paid or quota limited review requests after ordinary pushes.
- Each ready migration pull request receives no more than one configured repository review unless a material post review change requires a replacement review.
- Every merged migration pull request has successful required checks, resolved actionable feedback, and a mergeable head.
- All twelve open migration pull requests are repaired and merged, or retain a precise evidence backed blocker without weakened checks.
- Plans, documentation, Issues, Projects, milestones, and pull request state reflect the verified result.
- Organization hard zero dollar budgets remain enabled and no Copilot purchase or metered API review workflow is introduced.

## Final Organization Rollout Result

All 25 transferred caller repositories resolve under `MCEnvision`. Their default branch or active migration pull request head references the reviewed shared workflow commit `d731214d860ad2422ab8956a5d337dfaec51f64a`.

The four major action upgrades were reviewed and verified independently before merge. The central workflows now use `actions/setup-node` 7.0.0, `actions/checkout` 7.0.1, `actions/dependency-review-action` 5.0.0, and `actions/upload-artifact` 7.0.1 at full commit SHAs. The thirteen passing caller repositories were repinned through separate verified pull requests. Twelve migration pull requests remain drafts with automatic merge disabled because their own dependency, Gradle, compilation, test, or CodeQL gates fail. No failed caller was merged.

The organization remains on GitHub Team with two members and no outside collaborators. All Actions usage observed during the rollout was fully discounted or covered by included usage, leaving a net Actions charge of zero dollars. A billing audit found approximately $1.23 of Secret Protection usage that had already accrued on private repositories. Secret Protection, private push protection, and private advanced security were disabled on every private repository to stop further licensed usage. Hard zero dollar budgets continue to block metered Actions, Codespaces, Packages, and Git LFS overages.

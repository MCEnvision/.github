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

- [ ] Apply supported remote settings to owned active repositories.
- [x] Preserve local worktrees, active phase branches, forks, archives, and excluded repositories. Include example repositories only when they are explicitly placed in rollout scope.
- [x] Open signed draft caller-workflow migration pull requests for all 29 eligible repositories. Preserve repository-specific verification and replace only copied generic workflows.
- [x] Reconcile migration pull request review findings before merge.
  - Pin every reusable workflow call and its shared validation scripts to one reviewed central commit.
  - Isolate dependency submission and CodeQL into dedicated reusable workflows so skipped privileged jobs cannot elevate a read-only caller during workflow validation.
  - Grant write permissions only to trusted default-branch and manual runs.
  - Grant pull request validation the minimum read and security permissions required by enabled jobs.
  - Detect nested Node.js projects and run their locked checks from the correct working directory.
  - Omit disabled or default-only inputs so caller intent remains clear.
  - Preserve repository-specific smoke, schema, deployment, and release checks when they exceed the shared baseline.
- [x] Merge only migration pull requests with completed successful checks, no requested changes, no unresolved actionable feedback, and a mergeable head. Seventeen migration pull requests met the gate and merged.
- [x] Leave repositories with existing build, test, dependency, wrapper, or lint failures open for repository-specific repair. Twelve migration pull requests remain draft with automatic merge disabled.
- [ ] Verify zero remote drift after rollout.

## Phase 4. Continuous Reconciliation

- [x] Check all GitHub layers quietly at the start of every repository-scoped request.
- [x] Reconcile actionable review, security, dependency, CI, issue, Project, milestone, wiki, and release feedback.
- [x] Keep plans and canonical documentation synchronized with verified implementation.

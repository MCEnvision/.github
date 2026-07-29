# Implementation Plan

## Phase 1. Shared Workflow Foundation

- [x] Create the public, credential-free shared workflow repository.
- [x] Define the quality and release validation contracts.
- [x] Add deterministic validation scripts.
- [ ] Validate the workflows in GitHub Actions.
- [ ] Publish the verified initial baseline.

## Phase 2. Onboarding Integration

- [x] Replace copied CI and security workflows with thin shared-workflow callers.
- [x] Detect repository Java, Gradle, Node.js, GameTest, documentation, and CodeQL inputs.
- [x] Add rulesets, CODEOWNERS, environments, secret scanning, immutable releases, and supported attestations to onboarding.
- [x] Add signed commit and signed annotated tag requirements.
- [x] Add capability-aware fallback behavior that never creates permanently failing checks.

## Phase 3. Fleet Rollout

- [ ] Apply supported remote settings to owned active repositories.
- [ ] Preserve dirty worktrees, active phase branches, forks, archives, examples, and excluded repositories.
- [ ] Schedule caller-workflow migration through each repository's safe phase workflow.
- [ ] Verify zero remote drift after rollout.

## Phase 4. Continuous Reconciliation

- [x] Check all GitHub layers quietly at the start of every repository-scoped request.
- [x] Reconcile actionable review, security, dependency, CI, issue, Project, milestone, wiki, and release feedback.
- [x] Keep plans and canonical documentation synchronized with verified implementation.

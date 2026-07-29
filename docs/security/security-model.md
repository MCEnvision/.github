# Security Model

## Trust Boundaries

Caller repositories own source code, issue data, workflow permissions, environments, and secrets. This repository owns reusable workflow implementation and validation scripts.

Reusable workflows never receive credentials by default. Environment secrets remain in the caller repository and are exposed only to jobs that explicitly reference the environment.

## Pull Request Safety

- Pull request code never receives release credentials.
- Dependency submission runs only on trusted default-branch code.
- CodeQL and dependency review run only where GitHub supports their APIs.
- Secret scanning runs with read-only repository access.
- External actions are pinned to complete commit SHAs.
- GitHub enforces complete commit SHA pinning in the shared repository.
- Only GitHub owned actions and the audited Gradle, TruffleHog, Anchore, and OpenSSF repositories are allowed.
- A tracked validator rejects unknown publishers and mutable references before merge.

## Static Analysis

The shared repository scans Python and GitHub Actions with CodeQL security extended queries. Public Java and Kotlin callers can run the same suite. NeoForge callers can also enable the shared query pack for client class isolation, command permissions, packet validation, network bounds, and filesystem paths.

OpenSSF Scorecard publishes public supply chain findings to the Security tab. Findings remain advisory until verified against repository evidence.

## Credential Coverage

Native GitHub secret scanning and push protection are enabled where supported. Central scanning supplements native detection for credentials associated with GitHub, Discord, CurseForge, Modrinth, PostgreSQL, Cloudflare, Sentry, and other providers.

Never add test credentials that resemble working secrets. Use clearly invalid placeholders.

Organization custom secret patterns require GitHub Secret Protection. That separately licensed feature remains disabled under the zero additional spend rule. The central TruffleHog scan provides credential coverage without enabling a paid private repository feature.

## Runner Isolation

No public repository or fork pull request may execute on node1. A future node1 runner must be ephemeral, private repository only, assigned one job, isolated from long lived credentials, and wiped after completion.

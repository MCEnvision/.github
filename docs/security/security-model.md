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

## Credential Coverage

Native GitHub secret scanning and push protection are enabled where supported. Central scanning supplements native detection for credentials associated with GitHub, Discord, CurseForge, Modrinth, PostgreSQL, Cloudflare, Sentry, and other providers.

Never add test credentials that resemble working secrets. Use clearly invalid placeholders.

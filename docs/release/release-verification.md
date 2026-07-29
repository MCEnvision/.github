# Release Verification

Release validation produces:

- The exact release artifact set.
- SHA 256 and SHA 512 checksum inventories.
- A JSON manifest containing the source repository, commit, artifact sizes, and digests.
- An SPDX JSON software bill of materials.
- A retained GitHub Actions validation bundle.
- Build provenance and SBOM attestations when the repository plan supports them.
- A verified signed annotated tag for tag initiated releases.
- Verification that every public artifact attestation matches the caller repository, shared signer repository, release validation workflow, and artifact digest.

The publication workflow must consume the validated artifact set without rebuilding or replacing it. Immutable releases must be enabled before publication. Published release tags and assets are never moved or replaced.

Before an external upload, run:

```text
gh attestation verify --repo OWNER/REPOSITORY --signer-repo MCEnvision/.github --signer-workflow MCEnvision/.github/.github/workflows/release-validation.yml PATH
```

The command verifies the artifact digest and signer identity. A failed verification blocks GitHub Release, CurseForge, Modrinth, staging, and production publication.

Each publication target should create or update a GitHub Deployment containing the target version, source commit, artifact digest, environment, result, and rollback relationship.

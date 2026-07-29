# Release Verification

Release validation produces:

- The exact release artifact set.
- SHA-256 and SHA-512 checksum inventories.
- A JSON manifest containing the source repository, commit, artifact sizes, and digests.
- An SPDX JSON software bill of materials.
- A retained GitHub Actions validation bundle.
- Build provenance and SBOM attestations when the repository plan supports them.

The publication workflow must consume the validated artifact set without rebuilding or replacing it. Immutable releases must be enabled before publication. Published release tags and assets are never moved or replaced.

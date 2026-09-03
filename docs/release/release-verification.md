# Release Verification

Release validation produces:

- The exact release artifact set.
- SHA 256 and SHA 512 checksum inventories.
- A JSON manifest containing the source repository, commit, artifact sizes, and digests.
- An SPDX JSON software bill of materials.
- A retained GitHub Actions validation bundle.
- Build provenance and SBOM attestations when the repository plan supports them.
- A verified signed annotated tag for tag initiated releases.
- Separate verification of build provenance and SPDX SBOM attestations for every public artifact. Each check matches the caller repository, exact reusable workflow, source commit, and artifact digest.

The publication workflow must consume the validated artifact set without rebuilding or replacing it. Immutable releases must be enabled before publication. Published release tags and assets are never moved or replaced.

Before an external upload, run:

```text
gh attestation verify --repo OWNER/REPOSITORY --signer-workflow MCEnvision/.github/.github/workflows/release-validation.yml --source-digest COMMIT --predicate-type https://slsa.dev/provenance/v1 PATH
gh attestation verify --repo OWNER/REPOSITORY --signer-workflow MCEnvision/.github/.github/workflows/release-validation.yml --source-digest COMMIT --predicate-type https://spdx.dev/Document/v2.3 PATH
```

The workflow path identifies the shared signer repository and exact reusable workflow without combining incompatible GitHub CLI identity filters. The first command verifies build provenance. The second verifies the SPDX SBOM predicate. A failed verification blocks GitHub Release, CurseForge, Modrinth, staging, and production publication.

After the untouched artifact passes, the shared workflow copies each candidate outside the retained release bundle, changes one byte, and reruns both checks with `--expect-failure`. Both predicates must reject the altered copy. An accepted altered copy fails release validation.

The central release validation job records its selected GitHub environment. Each publication target must create or update a separate GitHub Deployment containing the target version, source commit, artifact digest, environment, result, and rollback relationship. The release broker owns those publication records because it receives the authoritative GitHub Release, CurseForge, Modrinth, staging, or production upload result.

---
name: release
description: Prepare or audit a GitHub, CurseForge, or Modrinth release with versioning, changelog, signed tag, checksums, SBOM, attestation, and deployment evidence.
---

Require explicit publication authorization. Confirm target version, channel, platforms, dependencies, and changelog range.

Build from the signed annotated tag. Validate artifact contents and generate SHA 256, SHA 512, source commit, SPDX, and attestation evidence.

Verify the attestation identity and digest before upload. Record each target as a GitHub Deployment. Never replace an immutable artifact or conceal a partial failure.
